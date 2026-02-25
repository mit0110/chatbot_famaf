from datetime import datetime, timezone
from beanie import Document, Link
from pymongo import IndexModel, ASCENDING
from app.models.answer import Answer


class Question(Document):
    """
    Entidad principal del FAQ. Cada pregunta tiene obligatoriamente
    una categoría y una respuesta asociada.
    """
    content: str
    category: str  # obligatorio
    answer: Link[Answer]  # obligatorio - referencia al documento Answer
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "questions"
        indexes = [
            IndexModel([("content", ASCENDING)], unique=True)
        ]