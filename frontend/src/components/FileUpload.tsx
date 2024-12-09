
import React, { useState } from 'react';

interface FileUploadProps {
  onUploadSuccess: (documentId: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUploadSuccess }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setUploadStatus('Upload successful');
      onUploadSuccess(data.document_id);
    } catch (error) {
      setUploadStatus('Upload failed');
    }
  };

  return (
    <div 
      className={`upload-area ${isDragging ? 'dragging' : ''}`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        handleUpload(file);
      }}
    >
      <h2>Drop your document here</h2>
      <p>Supported formats: PDF, DOCX, TXT</p>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={(e) => e.target.files && handleUpload(e.target.files[0])}
      />
      {uploadStatus && <p className="status-message">{uploadStatus}</p>}
    </div>
  );
};

export default FileUpload;