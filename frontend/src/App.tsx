import React, { useState, useEffect } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import ProcessingStatus from './components/ProcessingStatus.tsx';
import SummaryDisplay from './components/SummaryDisplay.tsx';


interface Summary {
  summary: string;
  key_points: string[];
  status: string;
  processing_time: number;
}

interface DocumentHistory {
  id: string;
  filename: string;
  upload_date: string;
}

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [message, setMessage] = useState('');
  const [processing, setProcessing] = useState(false);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [documentHistory, setDocumentHistory] = useState<DocumentHistory[]>([]);
  const [preferences, setPreferences] = useState({
    max_words: 200,
    paragraphs: 2
  });
  const [processingStatus, setProcessingStatus] = useState({
    state: 'idle' as 'idle' | 'processing' | 'completed' | 'failed',
    progress: 0,
    estimatedTime: 5
  });

  const validateFile = (file: File | undefined) => {
    if (!file) {
      setMessage('Error: No file selected');
      return false;
    }
  
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain'
    ];
    
    if (!allowedTypes.includes(file.type)) {
      setMessage('Error: Unsupported file type. Please upload PDF, DOCX, or TXT files.');
      return false;
    }
    return true;
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile && validateFile(droppedFile)) {
      await uploadFile(droppedFile);
    }
  };

  const uploadFile = async (file: File) => {
    setProcessing(true);
    setMessage('Uploading document...');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('max_words', preferences.max_words.toString());
    formData.append('paragraphs', preferences.paragraphs.toString());

    try {
        const response = await fetch('http://localhost:8000/api/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        setMessage(data.message);
        if (data.document_id) {
            checkSummaryStatus(data.document_id);
            setDocumentHistory(prev => [...prev, {
                id: data.document_id,
                filename: file.name,
                upload_date: new Date().toISOString()
            }]);
        }
    } catch (error) {
        setMessage('Upload failed: ' + (error instanceof Error ? error.message : String(error)));
    } finally {
        setProcessing(false);
    }
};

const checkSummaryStatus = async (documentId) => {
  const interval = setInterval(async () => {
      try {
          const response = await fetch(`http://localhost:8000/api/summary/${documentId}`);
          const data = await response.json();

          if (data.status === 'completed') {
              clearInterval(interval);
              setSummary({
                  summary: data.summary,
                  key_points: data.key_points,
                  status: data.status,
                  processing_time: data.processing_time
              });
              setProcessingStatus({
                  state: 'completed',
                  progress: 100, // 100% when completed
                  estimatedTime: 0
              });
              setProcessing(false);
          } else {
              setProcessingStatus({
                  state: 'processing',
                  progress: data.progress,
                  estimatedTime: data.estimated_time
              });
              setProcessing(true);
              setMessage(`Processing: ${data.progress}% complete. Estimated time: ${data.estimated_time}s`);
          }
      } catch (error) {
          setMessage('Error retrieving summary');
          setProcessingStatus({
              state: 'failed',
              progress: 0,
              estimatedTime: 0
          });
          clearInterval(interval);
      }
  }, 1000);
};

  

  return (
    <div className="app-container">
      <div className="chat-interface">
        <div className="preferences-section">
          <h3>Summary Preferences</h3>
          <div className="preference-inputs">
            <input 
              type="number" 
              value={preferences.max_words}
              onChange={(e) => setPreferences({...preferences, max_words: parseInt(e.target.value)})}
              placeholder="Max words"
              min="50"
              max="1000"
            />
            <input 
              type="number" 
              value={preferences.paragraphs}
              onChange={(e) => setPreferences({...preferences, paragraphs: parseInt(e.target.value)})}
              placeholder="Number of paragraphs"
              min="1"
              max="10"
            />
          </div>
        </div>
        
        <div 
          className={`upload-area ${isDragging ? 'dragging' : ''}`}
          onDragOver={(e) => {
            e.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          <h2>Drop your document here</h2>
          <p>Supported formats: PDF, DOCX, TXT</p>
          <input
            type="file"
            onChange={(e) => {
                const file = e.target.files?.[0];
                if (file && validateFile(file)) {
                uploadFile(file);
                }
            }}
            accept=".pdf,.docx,.txt"
            />
        </div>
        
        {processing && (
        <ProcessingStatus 
            status={{
            state: 'processing',
            progress: processingStatus.progress,
            estimatedTime: processingStatus.estimatedTime
            }}
        />
        )}

        {message && <div className="message">{message}</div>}

        {summary && (
        <SummaryDisplay 
            summary={{
            text: summary.summary,
            keyPoints: summary.key_points,
            processingTime: summary.processing_time // Add this to your Summary interface
            }}
        />
        )}

        {documentHistory.length > 0 && (
          <div className="document-history">
            <h3>Recent Documents</h3>
            <div className="history-list">
              {documentHistory.map(doc => (
                <div 
                  key={doc.id} 
                  className="history-item"
                  onClick={() => checkSummaryStatus(doc.id)}
                >
                  <span className="filename">{doc.filename}</span>
                  <span className="upload-date">
                    {new Date(doc.upload_date).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;