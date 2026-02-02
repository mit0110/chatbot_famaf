from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print('Connected to MongoDB...')

db = client[settings.MONGO_INITDB_DATABASE]
Question = db.questions
Answer = db.answers

# Índices únicos
Question.create_index([("content", pymongo.ASCENDING)], unique=True)

# Índices para mejorar performance en Answer (no únicos)
Answer.create_index([("content", pymongo.TEXT)])  # Búsqueda de texto completo
Answer.create_index([("created_at", pymongo.DESCENDING)])  # Ordenar por fecha
