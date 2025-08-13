This project is an AI-powered web application designed to help job seekers tailor their resumes for specific job descriptions. The tool analyzes a candidate's resume and a target job description, then generates an optimized resume that is more likely to pass through Applicant Tracking Systems (ATS). It also provides a detailed breakdown of the changes made, an ATS score, and suggestions for upskilling.

Feature: <br>
Resume Parsing: Accepts resume uploads in PDF and DOCX formats.<br>
AI-Powered Optimization: Utilizes a large language model (LLM) to compare the resume with a job description and suggest targeted improvements.<br>
ATS Score Calculation: Provides an estimated ATS score with a clear explanation of how it was calculated.<br>
Detailed Modifications: Summarizes the specific changes made, such as keyword incorporation and rephrased bullet points.<br>
Upskilling Suggestions: Identifies skill gaps and recommends relevant courses or certifications.<br>


Tech Stack:<br>
Frontend: React.js<br>
Backend: Flask<br>
AI Model: Google Gemini API<br>


Installation and Setup:<br>
Prerequisites;<br>
Node.js and npm installed on your machine.<br>
Python 3.8+ and pip installed.<br>

Navigate to the backend directory.<br>
cd backend<br>
python -m venv venv<br>
pip install -r requirements.txt<br>
python app.py<br>
The backend server will start on http://localhost:5000.<br>


Open a new terminal and navigate to the frontend directory.<br>
cd frontend<br>
npm install<br>
npm start<br>
The application will open in your browser, typically at http://localhost:3000.

I have deployed it in render and the url is : https://ai-resume-generator-0orm.onrender.com<br>

Incase if you running this locally, kindly do the following change:<br>
  In App.js inside src in frontend directory, change the fetch command in line 37 from https://ai-resume-generator-ta2j.onrender.com to http://localhost:5000/api/optimize. <br>
  In package.json in frontend directory, change the line 17 to "start": "react-scripts start"
  This enables the program to run locally. 



