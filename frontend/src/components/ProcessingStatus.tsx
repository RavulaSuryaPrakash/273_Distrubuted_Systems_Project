
import React from 'react';

interface ProcessingStatusProps {
  status: {
    state: 'processing' | 'completed' | 'failed';
    progress: number;
    estimatedTime?: number;
  };
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ status }) => {
  return (
    <div className="processing-status">
      <div className="status-indicator">
        {status.state === 'processing' && (
          <>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${status.progress}%` }}
              />
            </div>
            <p>Processing document... {status.progress}%</p>
            {status.estimatedTime && (
              <p>Estimated time remaining: {status.estimatedTime}s</p>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ProcessingStatus;