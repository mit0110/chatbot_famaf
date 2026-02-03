from pymongo import mongo_client
import pymongo
from app.config import settings
from datetime import datetime

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
Question = db.questions
Answer = db.answers
Category = db.categories

# Índices únicos
Question.create_index([("content", pymongo.ASCENDING)], unique=True)
Answer.create_index([("content", pymongo.ASCENDING)], unique=True)
Category.create_index([("name", pymongo.ASCENDING)], unique=True)

# Índices para mejorar performance en Answer
Answer.create_index([("created_at", pymongo.DESCENDING)])  # Ordenar por fecha

# Initialize default categories if collection is empty
DEFAULT_CATEGORIES = [
    "Información General",
    "Cursado",
    "Exámenes",
    "Ingreso",
    "Egreso",
    "Sin Información"
]

if Category.count_documents({}) == 0:
    for cat_name in DEFAULT_CATEGORIES:
        Category.insert_one({
            "name": cat_name,
            "created_at": datetime.utcnow()
        })
