from datetime import datetime, timezone
from typing import Optional
from beanie import Document, Link
from pymongo import IndexModel, ASCENDING
from app.models.answer import Answer


class Question(Document):
    content: str
    category: str | None = None
    answer: Optional[Link[Answer]] = None  # referencia real al documento Answer
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "questions"
        indexes = [
            IndexModel([("content", ASCENDING)], unique=True)
        ]