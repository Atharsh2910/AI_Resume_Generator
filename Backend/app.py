# app.py
import os
import io
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import docx
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure your Gemini API key here
# The API key will be automatically provided by the Canvas environment.
# DO NOT hardcode your API key here.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", None)
if not GEMINI_API_KEY:
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
# Allow CORS for all origins, which is necessary for production deployment.
CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def parse_resume_to_text(file_stream, filename):
    """
    Parses a resume file (PDF or DOCX) and returns its text content.
    """
    text = ""
    # Check for PDF file
    if filename.endswith('.pdf'):
        try:
            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            return f"Error parsing PDF: {e}"

    # Check for DOCX file
    elif filename.endswith('.docx'):
        try:
            doc = docx.Document(file_stream)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            return f"Error parsing DOCX: {e}"
    else:
        return "Unsupported file format. Please upload a PDF or DOCX."
    
    return text

def analyze_and_optimize(resume_text, job_description):
    """
    Uses the Gemini API to analyze the resume and job description
    and generate an optimized resume.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

        # This is the core prompt design. We instruct the model to act as a
        # professional resume writer and perform a series of tasks.
        prompt = f"""
        You are a highly skilled AI resume optimizer and career coach. Your task is to analyze a candidate's resume and a target job description.

        Analyze the following:
        1.  **Resume Content:** The candidate's resume text.
        2.  **Job Description:** The target job description.

        Based on your analysis, perform the following actions:
        -   **Optimized Resume:** Rewrite the resume to be highly tailored to the job description. Incorporate relevant keywords and rephrase bullet points to highlight skills and experience that match the job description.
        -   **ATS Score:** Provide an estimated ATS (Applicant Tracking System) score out of 100. Base this on keyword density, formatting, and the use of standard resume sections. Explain the score with specific details.
        -   **Modifications:** Summarize the key changes you made to the resume. This should be a bulleted list of modifications, such as "Added key skills from the job description," "Rephrased experience bullet points," and "Bolded important keywords."
        -   **Upskilling Suggestions:** Based on any gaps between the resume and the job description, suggest 3-5 relevant skills, courses, or certifications the candidate could pursue to be a better fit.

        The optimized resume should be a clean, text-based version without complex formatting, using markdown for structure (bolding, lists). The final response should be a single JSON object with the following keys: `optimized_resume`, `ats_score`, `modifications`, and `upskilling_suggestions`.

        **Candidate Resume:**
        {resume_text}

        **Job Description:**
        {job_description}
        """

        response = model.generate_content(prompt)
        
        # The API response is expected to be a stringified JSON object.
        # We need to parse it back into a Python dictionary.
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
    file_stream = io.BytesIO(resume_file.read())

    # Parse resume to text
    resume_text = parse_resume_to_text(file_stream, filename)
    if resume_text.startswith("Error"):
        return jsonify({"error": resume_text}), 500
    
    # Call the AI model for optimization
    response_data = analyze_and_optimize(resume_text, job_description)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # To run this file, use: python app.py
    app.run(debug=True, port=5000)
