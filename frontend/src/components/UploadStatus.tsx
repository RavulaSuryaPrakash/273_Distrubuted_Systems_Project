// frontend/src/components/UploadStatus.tsx
import React from 'react';

interface UploadStatusProps {
    status: string;
    progress: number;
}

const UploadStatus: React.FC<UploadStatusProps> = ({ status, progress }) => {
    return (
        <div className="upload-status">
            <div className="status-message">{status}</div>
            <div className="progress-bar">
                <div 
                    className="progress-fill" 
                    style={{ width: `${progress}%` }}
                />
            </div>
        </div>
    );
};

export default UploadStatus;