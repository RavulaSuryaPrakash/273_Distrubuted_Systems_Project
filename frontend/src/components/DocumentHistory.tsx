// frontend/src/components/DocumentHistory.tsx
import React, { useState, useEffect } from 'react';

interface Document {
    document_id: string;
    filename: string;
    upload_date: string;
    status: string;
}

const DocumentHistory: React.FC = () => {
    const [history, setHistory] = useState<Document[]>([]);

    const fetchHistory = async () => {
        const response = await fetch('http://localhost:8000/api/documents/history');
        const data = await response.json();
        setHistory(data);
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    return (
        <div className="document-history">
            <h3>Document History</h3>
            {history.map((doc: Document) => (
                <div key={doc.document_id} className="history-item">
                    <span>{doc.filename}</span>
                    <span>{doc.upload_date}</span>
                    <span>{doc.status}</span>
                </div>
            ))}
        </div>
    );
};

export default DocumentHistory;