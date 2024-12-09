# backend/services/database.py
from typing import Dict, List
from datetime import datetime
import asyncio
import json

from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, String, Text, JSON, Integer, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

# Database URL (adjust username/password/host as needed)
DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost/doc_summarizer"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Metadata and Table Definitions
metadata = MetaData()

summaries = Table(
    "summaries",
    metadata,
    Column("document_id", UUID(as_uuid=True), primary_key=True),
    Column("summary", Text, nullable=False),
    Column("key_points", JSON, nullable=False),
    Column("original_text", Text, nullable=False),
    Column("processing_time", Float, nullable=False),
    Column("status", String(50), nullable=False, default="processing"),
    Column("requested_words", Integer, nullable=False),
    Column("requested_paragraphs", Integer, nullable=False),
    Column("actual_word_count", Integer, nullable=False),
    Column("actual_paragraphs", Integer, nullable=False),
    Column("created_at", TIMESTAMP, default="now()")
)

# Async Session Factory
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Asynchronous Table Creation Function
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

# Initialize Database Instance
database = Database(DATABASE_URL)

class DatabaseService:
    @staticmethod
    async def save_summary(document_id: str, summary_data: dict):
        query = summaries.insert().values(
            document_id=document_id,
            summary=summary_data["summary"],
            key_points=summary_data["key_points"],
            original_text=summary_data["original_text"],
            processing_time=summary_data["processing_time"],
            status=summary_data["status"],
            requested_words=summary_data["requested_words"],
            requested_paragraphs=summary_data["requested_paragraphs"],
            actual_word_count=summary_data["actual_word_count"],
            actual_paragraphs=summary_data["actual_paragraphs"]
        )
        await database.execute(query)

    @staticmethod
    async def get_summary(document_id: str):
        query = summaries.select().where(summaries.c.document_id == document_id)
        return await database.fetch_one(query)
    
    @staticmethod
    async def update_task_status(document_id: str, status: str):
        query = summaries.update().where(summaries.c.document_id == document_id).values(status=status)
        await database.execute(query)

    def _load_summaries(self) -> Dict[str, Dict]:
        try:
            with open(self.summaries_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_summaries(self, summaries: Dict[str, Dict]) -> None:
        with open(self.summaries_file, 'w') as f:
            json.dump(summaries, f)