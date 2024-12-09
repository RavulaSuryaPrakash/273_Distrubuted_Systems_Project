// frontend/src/components/AccessibleUpload.tsx
import React from 'react';

const AccessibleUpload: React.FC = () => {
    return (
        <div 
            role="region" 
            aria-label="Document upload section"
            className="accessible-upload"
        >
            <label htmlFor="fileInput" className="upload-label">
                Upload Document
                <span className="tooltip">
                    Supported formats: PDF, DOCX, TXT
                </span>
            </label>
            <input
                id="fileInput"
                type="file"
                aria-describedby="fileHelpText"
                accept=".pdf,.docx,.txt"
            />
            <div id="fileHelpText" className="help-text">
                Drag and drop your file here or click to browse
            </div>
        </div>
    );
};

export default AccessibleUpload;