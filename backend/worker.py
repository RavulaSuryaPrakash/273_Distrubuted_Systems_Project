import asyncio
import time
import aio_pika
import json

from services.summarizer import SummarizationService
from services.database import database, DatabaseService

# Initialize services
summarization_service = SummarizationService()
db_service = DatabaseService()

async def main():
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        # Connect to the database
        await database.connect()
        print("Database connected successfully")
        # Create a channel
        channel = await connection.channel()

        # Declare a queue
        queue = await channel.declare_queue("document_queue", durable=False)

        # Consume messages from the queue
        async for message in queue:
            async with message.process():
                task = json.loads(message.body)
                await process_task(task)

async def process_task(task):
    try:
        document_id = task["document_id"]
        text_content = task["text_content"]
        max_words = task["max_words"]
        paragraphs = task["paragraphs"]

        print(f"Processing document ID: {document_id}")

        # Update task status to "processing" in the database
        await DatabaseService.update_task_status(document_id, "processing")

        # Generate summary
        summary_result = await summarization_service.generate_summary(
            text_content,
            max_words=max_words,
            num_paragraphs=paragraphs
        )

        # Log generated summary
        print(f"Generated summary for {document_id}: {summary_result}")

        # Save summary
        print(f"Saving summary for document ID {document_id}")
        await DatabaseService.save_summary(document_id, {
            "summary": summary_result["summary"],
            "key_points": summary_result["key_points"],
            "original_text": text_content,
            "processing_time": time.time(),
            "status": "completed",  # Set status as 'completed'
            "requested_words": max_words,
            "requested_paragraphs": paragraphs,
            "actual_word_count": summary_result.get("word_count", 0),
            "actual_paragraphs": summary_result.get("actual_paragraphs", 0)
        })

        # Update task status to "completed" in the database
        await DatabaseService.update_task_status(document_id, "completed")

        print(f"Document {document_id} processed and saved successfully")

    except Exception as e:
        print(f"Error processing task for document ID {document_id}: {str(e)}")
        # Optionally, update the status to "failed" if there's an error
        await DatabaseService.update_task_status(document_id, "failed")

if __name__ == "__main__":
    asyncio.run(main())