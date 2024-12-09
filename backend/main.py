import asyncio
import logging
from typing import Annotated, Optional
import uuid
import time
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, logger
from fastapi.middleware.cors import CORSMiddleware
import pika
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
#from services.rabbitmq_service import RabbitMQService
from services.document_processor import DocumentProcessor
from services.summarizer import SummarizationService 
from services.status_tracker import StatusTracker
from services.database import DatabaseService
from services.database import database, create_tables

from datetime import datetime
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


from fastapi import FastAPI
from services.database import database, create_tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Connect to the database and create tables
    await database.connect()
    await create_tables()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"


# Initialize in-memory storage
summaries = {}
processing_status = {}

# Initialize services
document_processor = DocumentProcessor()
summarization_service = SummarizationService()
db_service = DatabaseService()


async def get_processing_status(document_id: str):
    """Get the processing status for a document"""
    if document_id in summaries:  # Assuming `summaries` is where completed tasks are stored
        return {
            "status": "completed",
            "progress": 100,
            "estimated_time": 0,
            "summary": summaries[document_id]["summary"]  # Send the generated summary
        }
    else:
        return {
            "status": "processing",
            "progress": 50,
            "estimated_time": 5
        }
# RabbitMQ connection
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='document_queue')  # Declare the queue
    return connection, channel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(...),
    max_words: Optional[int] = Form(default=200),
    paragraphs: Optional[int] = Form(default=2)
):
    try:
        logger.debug(f"Received file: {file.filename}")
        content = await file.read()

        # Process file content (basic validation)
        if file.content_type == 'text/plain':
            text_content = content.decode('utf-8')
        else:
            text_content = await document_processor.process_document(content, file.content_type)

        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Create a message payload
        message_payload = {
            "document_id": document_id,
            "text_content": text_content,
            "max_words": max_words,
            "paragraphs": paragraphs,
            "filename": file.filename,
        }

        # Connect to RabbitMQ and publish the message
        connection, channel = setup_rabbitmq()
        channel.basic_publish(
            exchange='',
            routing_key='document_queue',
            body=json.dumps(message_payload)
        )
        connection.close()

        logger.debug("Task added to RabbitMQ queue")

        # Return response with document ID
        return {
            "message": "Document uploaded successfully and queued for processing",
            "document_id": document_id,
            "status": "processing"
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.get("/api/summary/{document_id}")
async def fetch_summary(document_id: str):
    try:
        logger.debug(f"Fetching summary for document ID {document_id}")
        summary = await DatabaseService.get_summary(document_id)  # Call the database method
        
        if not summary:
            logger.debug(f"Summary for document ID {document_id} is still processing")
            return {
                "status": "",
                "message": "Summary is being generated",
                "document_id": document_id,
                "progress": 50,
                "estimated_time": 5
            }
        
        logger.debug(f"Summary for document ID {document_id} is completed")
        return {
            "status": "completed",
            "progress": 100,
            "document_id": summary["document_id"],
            "summary": summary["summary"],
            "key_points": summary["key_points"],
            "original_text": summary["original_text"],
            "processing_time": summary["processing_time"],
            "requested_words": summary["requested_words"],
            "requested_paragraphs": summary["requested_paragraphs"],
            "actual_word_count": summary["actual_word_count"],
            "actual_paragraphs": summary["actual_paragraphs"],
            "created_at": summary["created_at"]
        }
    except Exception as e:
        logger.error(f"Error retrieving summary for document ID {document_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving summary: {str(e)}"
        )
        
    
    

@app.websocket("/ws/{document_id}")
async def websocket_endpoint(websocket: WebSocket, document_id: str):
    await websocket.accept()
    try:
        while True:
            status = await get_processing_status(document_id)  # Use the right function to track status
            await websocket.send_json(status)

            if status["status"] == "completed":
                break

            await asyncio.sleep(1)  # Sleep to avoid flooding the client with too many requests
    except WebSocketDisconnect:
        print(f"Client {document_id} disconnected")
