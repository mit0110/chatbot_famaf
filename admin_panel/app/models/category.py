from datetime import datetime, timezone
from beanie import Document
from pymongo import IndexModel, ASCENDING


class Category(Document):
    name: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        name = "categories"  # nombre de la colección en MongoDB
        indexes = [
            IndexModel([("name", ASCENDING)], unique=True)
        ]