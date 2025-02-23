import React, { useState } from 'react';
import { Loader2, AlertTriangle, ShieldCheck } from 'lucide-react';

const GmailAnalysis = () => {
    const [analyzing, setAnalyzing] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const analyzeGmail = async () => {
        try {
            setAnalyzing(true);
            setError(null);
            
            const response = await fetch('http://localhost:5000/test-gmail-fetch');
            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message);
            }
            
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <div className="gmail-analysis">
            <button 
                onClick={analyzeGmail}
                disabled={analyzing}
                className="analyze-button"
            >
                {analyzing ? (
                    <>
                        <Loader2 className="loading-spinner" size={20} />
                        Analyzing Gmail...
                    </>
                ) : (
                    'Analyze Gmail'
                )}
            </button>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {results && results.emails && (
                <div className="results">
                    <h3>Analysis Results ({results.count} emails)</h3>
                    {results.emails.map((email, index) => (
                        <div key={index} className="email-result">
                            <h4>{email.subject}</h4>
                            <p className="sender">From: {email.sender}</p>
                            <div className="analysis">
                                <div className="confidence-score">
                                    {email.analysis.is_legit ? (
                                        <ShieldCheck size={20} className="icon-safe" />
                                    ) : (
                                        <AlertTriangle size={20} className="icon-danger" />
                                    )}
                                    <span>
                                        Confidence Score: {Math.round(email.analysis.confidence_score * 100)}%
                                    </span>
                                </div>
                                <p className="analysis-text">{email.analysis.analysis}</p>
                                {email.analysis.suspicious_phrases?.length > 0 && (
                                    <div className="suspicious-phrases">
                                        <h5>Suspicious Elements:</h5>
                                        <ul>
                                            {email.analysis.suspicious_phrases.map((phrase, i) => (
                                                <li key={i}>{phrase}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default GmailAnalysis;