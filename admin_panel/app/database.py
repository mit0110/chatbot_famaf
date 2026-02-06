from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings

# Asynchronous MongoDB client for Beanie (FastAPI Users)
motor_client = AsyncIOMotorClient(settings.DATABASE_URL)
motor_db = motor_client[settings.MONGO_INITDB_DATABASE]


async def init_db():
    """Inicializar Beanie con el modelo User"""
    from app.models.users import User

    await init_beanie(
        database=motor_db,
        document_models=[User],
    )
    print('Beanie initialized for User authentication...')


# ============ DEPRECATED - Using Beanie for all databases ============
# from pymongo import mongo_client
# import pymongo
# from datetime import datetime
#
# # Synchronous MongoDB client (for backward compatibility)
# client = mongo_client.MongoClient(settings.DATABASE_URL)
# print('Connected to MongoDB...')
#
# db = client[settings.MONGO_INITDB_DATABASE]
# Question = db.questions
# Answer = db.answers
# Category = db.categories
#
# # Índices únicos
# Question.create_index([("content", pymongo.ASCENDING)], unique=True)
# Answer.create_index([("content", pymongo.ASCENDING)], unique=True)
# Category.create_index([("name", pymongo.ASCENDING)], unique=True)
#
# # Índices para mejorar performance en Answer
# Answer.create_index([("created_at", pymongo.DESCENDING)])  # Ordenar por fecha
#
# # Initialize default categories if collection is empty
# DEFAULT_CATEGORIES = [
#     "Información General",
#     "Cursado",
#     "Exámenes",
#     "Ingreso",
#     "Egreso",
#     "Sin Información"
# ]
#
# if Category.count_documents({}) == 0:
#     for cat_name in DEFAULT_CATEGORIES:
#         Category.insert_one({
#             "name": cat_name,
#             "created_at": datetime.utcnow()
#         })
