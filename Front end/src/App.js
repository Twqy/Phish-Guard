import React, { useState } from 'react';
import { ShieldCheck } from 'lucide-react';
import EmailInput from './components/EmailInput';
import ResultDisplay from './components/ResultDisplay';

function App() {
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleAnalyze = async (formData) => {
        setIsLoading(true);
        setError(null);
        
        try {
            const response = await fetch('http://localhost:5000/analyze-with-files', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('Analysis failed');
            
            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError('Failed to analyze content: ' + err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="header">
                <div className="header-content">
                    <ShieldCheck size={40} style={{ color: '#3b82f6' }} />
                    <h1 className="title">Phish Guard</h1>
                </div>
                <p className="description">
                    Protect yourself from phishing attempts. Paste any suspicious email 
                    to instantly analyze its authenticity with our advanced detection system.
                </p>
            </div>
            
            <div>
                <EmailInput onAnalyze={handleAnalyze} isLoading={isLoading} />
                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}
                {result && <ResultDisplay result={result} />}
            </div>
        </div>
    );
}

export default App;