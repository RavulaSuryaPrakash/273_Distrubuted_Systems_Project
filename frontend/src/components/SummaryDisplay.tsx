// frontend/src/components/SummaryDisplay.tsx
import React from 'react';

// components/SummaryDisplay.tsx
interface SummaryDisplayProps {
    summary: {
      text: string;
      keyPoints: string[];
      processingTime: number;
    };
  }
  
  const SummaryDisplay: React.FC<SummaryDisplayProps> = ({ summary }) => {
    return (
      <div className="summary-container">
        <h3>Summary</h3>
        <div className="summary-text">
          {summary.text}
        </div>
        
        <h3>Key Points</h3>
        <ul className="key-points">
          {summary.keyPoints.map((point, index) => (
            <li key={index}>{point}</li>
          ))}
        </ul>
        
        <div className="processing-info">
          Processing time: {summary.processingTime.toFixed(2)}s
        </div>
      </div>
    );
  };
  
  export default SummaryDisplay;