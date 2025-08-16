import os
import io
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import google.generativeai as genai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx2txt

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://ai-resume-generator-4u9k.onrender.com"]}})


def parse_resume_to_text(file_content, filename):
    """
    Extracts raw text from PDF or DOCX resume files.
    """
    try:
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()

        elif filename.lower().endswith(".docx"):
            # Save temp file to extract DOCX text
            temp_path = f"/tmp/{filename}"
            with open(temp_path, "wb") as f:
                f.write(file_content)
            text = docx2txt.process(temp_path)
            os.remove(temp_path)
            return text.strip()

        else:
            return "Error: Unsupported file type. Please upload PDF or DOCX."

    except Exception as e:
        app.logger.error(f"Resume parsing failed: {e}")
        return f"Error parsing file: {e}"


def analyze_and_optimize(resume_text, job_description):
    """
    Uses the Gemini API to analyze the resume and job description
    and generate an optimized resume.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

        prompt = f"""
        You are a highly skilled AI resume optimizer and career coach. Your task is to analyze a candidate's resume and a target job description.

        Analyze the following:
        1. **Resume Content:** The candidate's resume text.
        2. **Job Description:** The target job description.

        Based on your analysis, perform the following actions:
        - **Optimized Resume:** Rewrite the resume to be highly tailored to the job description. Incorporate relevant keywords and rephrase bullet points to highlight skills and experience that match the job description.
        - **ATS Score:** Provide an estimated ATS (Applicant Tracking System) score out of 100. Base this on keyword density, formatting, and the use of standard resume sections. Explain the score with specific details.
        - **Modifications:** Summarize the key changes you made to the resume. This should be a bulleted list of modifications, such as "Added key skills from the job description," "Rephrased experience bullet points," and "Bolded important keywords."
        - **Upskilling Suggestions:** Based on any gaps between the resume and the job description, suggest 3-5 relevant skills, courses, or certifications the candidate could pursue to be a better fit.

        The optimized resume should be a clean, text-based version without complex formatting, using markdown for structure (bolding, lists). The final response should be a single JSON object with the following keys: `optimized_resume`, `ats_score`, `modifications`, and `upskilling_suggestions`.

        **Candidate Resume:**
        {resume_text}

        **Job Description:**
        {job_description}
        """

        response = None
        for i in range(5):  # retry loop
            try:
                response = model.generate_content(prompt)
                break
            except Exception as e:
                app.logger.warning(f"Gemini API call failed, retrying... Attempt {i+1}/5. Error: {e}")
                time.sleep(2 ** i)

        if not response:
            return {"error": "Failed to get a response from the Gemini API after multiple retries."}

        response_json_str = response.text.strip('` \n').replace('json\n', '', 1)

        try:
            result = json.loads(response_json_str)
            return result
        except json.JSONDecodeError as e:
            app.logger.error(f"Failed to parse JSON from API response: {e}")
            app.logger.error(f"Raw API response: {response.text}")
            return {"error": "Failed to process the response from the AI model."}

    except Exception as e:
        app.logger.error(f"Gemini API call failed: {e}")
        return {"error": f"An error occurred with the AI service: {e}"}


@app.route('/api/optimize', methods=['POST'])
def optimize_resume():
    """
    Main API endpoint to receive files and process the request.
    """
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file part"}), 400

    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')

    if resume_file.filename == '':
        return jsonify({"error": "No selected resume file"}), 400

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    filename = secure_filename(resume_file.filename)
    file_content = resume_file.read()

    resume_text = parse_resume_to_text(file_content, filename)
    if resume_text.startswith("Error"):
        return jsonify({"error": resume_text}), 500

    response_data = analyze_and_optimize(resume_text, job_description)

    return jsonify(response_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
