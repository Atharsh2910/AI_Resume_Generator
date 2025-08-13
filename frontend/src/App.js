import React, { useState } from 'react';

// Main App component
const App = () => {
    // State variables to manage user input and application state
    const [resumeFile, setResumeFile] = useState(null);
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    // Handle file selection
    const handleFileChange = (e) => {
        setResumeFile(e.target.files[0]);
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResults(null);
        setError(null);

        // Check if both files and job description are provided
        if (!resumeFile || !jobDescription) {
            setError("Please upload a resume and provide a job description.");
            setLoading(false);
            return;
        }

        // Use FormData to send both the file and text to the backend
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job_description', jobDescription);

        try {
            const response = await fetch('https://ai-resume-generator-ta2j.onrender.com', {
                method: 'POST',
                body: formData,
            });

            // Handle non-200 responses
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Something went wrong with the API.');
            }

            const data = await response.json();
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // JSX for the component
    return (
        <div className="main-container">
            <header className="header">
                <h1>An AI resume generator</h1>
                <p>Upload your resume and the target job description! I will help you create a perfect resume tailored for the job!</p>
            </header>

            {/* Input Section */}
            <form onSubmit={handleSubmit} className="input-section">
                <h2>Setup Your Profile </h2>
                <div className="form-grid">
                    {/* Resume Input */}
                    <div className="form-group">
                        <label>
                            Upload Resume (PDF or DOCX)
                        </label>
                        <input
                            type="file"
                            accept=".pdf,.docx"
                            onChange={handleFileChange}
                        />
                    </div>
                    {/* Job Description Input */}
                    <div className="form-group">
                        <label>
                            Paste Job Description
                        </label>
                        <textarea
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            rows="4"
                            placeholder="Paste the job description here..."
                        ></textarea>
                    </div>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center' }}>
                    <button
                        type="submit"
                        disabled={loading}
                        className="submit-button"
                    >
                        {loading ? 'Analyzing...' : 'Analyze & Optimize'}
                    </button>
                </div>
            </form>

            {/* Chatbot Output Section */}
            <div className="output-section">
                <h2>AI Assistant Response</h2>
                {error && (
                    <div className="error-message">
                        <p>An error occurred: {error}</p>
                    </div>
                )}
                {results ? (
                    <div className="results-container">
                        <div className="result-card">
                            <div className="result-item">
                                <h3>ATS Score: <span className="score">{results.ats_score}</span></h3>
                                <p>{results.ats_score_explanation}</p>
                            </div>
                            <div className="result-item">
                                <h3>Modifications Made</h3>
                                <ul className="modifications-list">
                                    {Array.isArray(results.modifications) ? (
                                        results.modifications.map((item, index) => (
                                            <li key={index}>{item.replace(/^- /, '')}</li>
                                        ))
                                    ) : (
                                        results.modifications.split('\n').map((item, index) => (
                                            <li key={index}>{item.replace(/^- /, '')}</li>
                                        ))
                                    )}
                                </ul>
                            </div>
                            <div className="result-item">
                                <h3>Upskilling Suggestions</h3>
                                <ul className="upskilling-list">
                                    {Array.isArray(results.upskilling_suggestions) ? (
                                        results.upskilling_suggestions.map((item, index) => (
                                            <li key={index}>{item.replace(/^- /, '')}</li>
                                        ))
                                    ) : (
                                        results.upskilling_suggestions.split('\n').map((item, index) => (
                                            <li key={index}>{item.replace(/^- /, '')}</li>
                                        ))
                                    )}
                                </ul>
                            </div>
                        </div>
                        <div className="optimized-resume-container">
                            <h3>Optimized Resume</h3>
                            <pre className="optimized-resume">
                                {results.optimized_resume}
                            </pre>
                        </div>
                    </div>
                ) : (
                    <div className="text-gray-400">
                        Hey there! I'm your AI resume generator. Upload your resume, set job details, and let's get started! 
                    </div>
                )}
            </div>
        </div>
    );
};

export default App;
