import React from 'react';
import { CheckCircle, AlertTriangle, Gauge } from 'lucide-react';
import SuspiciousPhrases from './SuspiciousPhrases';

const ResultDisplay = ({ result }) => {
  const confidencePercentage = Math.round((parseFloat(result.confidence_score) || 0) * 100);
  const isLegitimate = confidencePercentage >= 50;

  const getVerdict = () => {
    if (confidencePercentage >= 80) {
      return "This email appears to be legitimate with high confidence.";
    } else if (confidencePercentage >= 50) {
      return "This email is likely legitimate, but exercise normal caution.";
    } else if (confidencePercentage >= 20) {
      return "This email shows signs of being a phishing attempt. Exercise extreme caution.";
    } else {
      return "This email is very likely a phishing attempt. Do not interact with any links or requests.";
    }
  };

  return (
    <div className="result-container">
      <div className="result-content">
        <div className="result-header">
          <div className="result-title-section">
            <h2 className="result-title">Analysis Results</h2>
            <div className="confidence-score">
              <Gauge size={24} style={{ color: '#3b82f6' }} />
              <span>{confidencePercentage}% Legitimate</span>
            </div>
          </div>
          
          <div className={`verdict-box ${isLegitimate ? 'safe' : 'danger'}`}>
            <h3 className="verdict-title">Verdict</h3>
            <p className="verdict-text">{getVerdict()}</p>
          </div>

          <div className={`result-box ${isLegitimate ? 'safe' : 'danger'}`}>
            {isLegitimate ? (
              <CheckCircle size={24} className="icon-safe" />
            ) : (
              <AlertTriangle size={24} className="icon-danger" />
            )}
            <div>
              <h3 className={isLegitimate ? 'text-safe' : 'text-danger'}>
                {isLegitimate ? 'Email Appears Safe' : 'Potential Phishing Detected'}
              </h3>
              <p className="analysis-text">{result.analysis}</p>
            </div>
          </div>
        </div>
      </div>
      
      {!isLegitimate && (
        <div className="result-sidebar">
          <SuspiciousPhrases phrases={result.suspicious_phrases} />
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;