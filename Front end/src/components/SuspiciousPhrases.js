import React from 'react';
import { AlertOctagon } from 'lucide-react';

const SuspiciousPhrases = ({ phrases }) => {
    if (!phrases || phrases.length === 0) return null;

    return (
        <div className="suspicious-phrases">
            <div className="suspicious-header">
                <AlertOctagon size={20} className="icon-danger" />
                <h3>Suspicious Elements</h3>
            </div>
            <div className="phrases-list">
                {phrases.map((phrase, index) => (
                    <div key={index} className="phrase-item">
                        <q className="phrase-text">{phrase.text}</q>
                        <p className="phrase-reason">{phrase.reason}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SuspiciousPhrases;