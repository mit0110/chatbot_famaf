from datetime import datetime, timezone
from beanie import Document
from pymongo import IndexModel, ASCENDING, DESCENDING


class Answer(Document):
    """
    Respuesta asociada a una o más preguntas.
    La categoría se hereda de la Question que la referencia.
    """
    content: str
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "answers"
        indexes = [
            IndexModel([("content", ASCENDING)], unique=True),
            IndexModel([("created_at", DESCENDING)]),
        ]