import React, { useState, useCallback } from 'react';
import { Shield, Loader2, Upload } from 'lucide-react';

const EmailInput = ({ onAnalyze, isLoading }) => {
    const [emailText, setEmailText] = useState('');
    const [files, setFiles] = useState([]);
    const [pastedImages, setPastedImages] = useState([]);

    const handlePaste = useCallback(async (e) => {
        const items = e.clipboardData?.items;
        if (!items) return;

        const imageItems = Array.from(items).filter(item => 
            item.type.indexOf('image') !== -1
        );

        for (const item of imageItems) {
            const file = item.getAsFile();
            if (file) {
                // Create preview URL
                const reader = new FileReader();
                reader.onload = (e) => {
                    setPastedImages(prev => [...prev, {
                        file,
                        preview: e.target.result
                    }]);
                };
                reader.readAsDataURL(file);
            }
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const formData = new FormData();
        formData.append('email', emailText);
        
        // Add regular uploaded files
        files.forEach(file => {
            formData.append('files', file);
        });
        
        // Add pasted images
        pastedImages.forEach(({file}, index) => {
            formData.append('files', file, `pasted-image-${index}.png`);
        });

        onAnalyze(formData);
    };

    const handleFileChange = (e) => {
        setFiles(Array.from(e.target.files));
    };

    const removeImage = (index) => {
        setPastedImages(prev => prev.filter((_, i) => i !== index));
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <textarea
                value={emailText}
                onChange={(e) => setEmailText(e.target.value)}
                onPaste={handlePaste}
                placeholder="Paste your email content or image here... "
                className="input-area"
                disabled={isLoading}
                rows="8"
            />
            
            {pastedImages.length > 0 && (
                <div className="pasted-images">
                    {pastedImages.map((image, index) => (
                        <div key={index} className="pasted-image-container">
                            <img 
                                src={image.preview} 
                                alt={`Pasted ${index}`} 
                                className="pasted-image"
                            />
                            <button
                                type="button"
                                onClick={() => removeImage(index)}
                                className="remove-image"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}
            
            <div className="file-upload-section">
                <label className="file-input-label">
                    <Upload size={20} />
                    <span>Add Attachments</span>
                    <input
                        type="file"
                        multiple
                        onChange={handleFileChange}
                        disabled={isLoading}
                        className="file-input"
                    />
                </label>
                {files.length > 0 && (
                    <div className="file-list">
                        {files.map((file, index) => (
                            <div key={index} className="file-item">
                                {file.name}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <button
                type="submit"
                disabled={isLoading || (!emailText.trim() && files.length === 0 && pastedImages.length === 0)}
                className={`button ${isLoading || (!emailText.trim() && files.length === 0 && pastedImages.length === 0) ? '' : 'button-primary'}`}
            >
                {isLoading ? (
                    <>
                        <Loader2 size={20} className="animate-spin" />
                        Analyzing...
                    </>
                ) : (
                    <>
                        <Shield size={20} />
                        Analyze Content
                    </>
                )}
            </button>
        </form>
    );
};

export default EmailInput;