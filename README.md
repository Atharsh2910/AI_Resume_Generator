This project is an AI-powered web application designed to help job seekers tailor their resumes for specific job descriptions. The tool analyzes a candidate's resume and a target job description, then generates an optimized resume that is more likely to pass through Applicant Tracking Systems (ATS). It also provides a detailed breakdown of the changes made, an ATS score, and suggestions for upskilling.

Feature:
Resume Parsing: Accepts resume uploads in PDF and DOCX formats.
AI-Powered Optimization: Utilizes a large language model (LLM) to compare the resume with a job description and suggest targeted improvements.
ATS Score Calculation: Provides an estimated ATS score with a clear explanation of how it was calculated.
Detailed Modifications: Summarizes the specific changes made, such as keyword incorporation and rephrased bullet points.
Upskilling Suggestions: Identifies skill gaps and recommends relevant courses or certifications.


Tech Stack:
Frontend: React.js
Backend: Flask
AI Model: Google Gemini API


Installation and Setup:
Prerequisites;
Node.js and npm installed on your machine.
Python 3.8+ and pip installed.

Navigate to the backend directory.
cd backend
python -m venv venv
pip install -r requirements.txt
python app.py
The backend server will start on http://localhost:5000.


Open a new terminal and navigate to the frontend directory.
cd frontend
npm install
npm start
The application will open in your browser, typically at http://localhost:3000.





