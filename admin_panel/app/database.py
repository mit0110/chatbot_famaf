from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.utils import DEFAULT_CATEGORIES

async def init_db():
    # Motor es el driver async de MongoDB, Beanie lo usa internamente
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.MONGO_INITDB_DATABASE]

    # Importamos los modelos acá para evitar imports circulares
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.category import Category

    # Beanie registra los modelos y crea los índices automáticamente
    await init_beanie(
        database=db,
        document_models=[Question, Answer, Category]
    )

    # Seed de categorías por defecto
    await seed_default_categories()

async def seed_default_categories():
    from app.models.category import Category

    count = await Category.count()
    if count == 0:
        for cat_name in DEFAULT_CATEGORIES:
            await Category(name=cat_name).insert()