from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from fastapi_users.password import PasswordHelper

from app.utils import DEFAULT_CATEGORIES

async def init_db():
    # Motor es el driver async de MongoDB, Beanie lo usa internamente
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.MONGO_INITDB_DATABASE]

    # Importamos los modelos acá para evitar imports circulares
    from app.models.question import Question
    from app.models.answer import Answer
    from app.models.category import Category
    from app.models.users import User

    # Beanie registra los modelos y crea los índices automáticamente
    await init_beanie(
        database=db,
        document_models=[Question, Answer, Category, User]
    )
    print('Beanie initialized for User authentication...')

    # Seed de categorías por defecto
    await seed_default_categories()

    # Crear superusuario inicial si no existe
    await create_initial_superuser()

async def seed_default_categories():
    from app.models.category import Category
    from datetime import datetime

    count = await Category.count()
    if count == 0:
        for cat_name in DEFAULT_CATEGORIES:
            await Category(name=cat_name).insert()


async def create_initial_superuser():
    """
    Crea un superusuario inicial si no existe ningún usuario en la base de datos.

    Utiliza las credenciales definidas en las variables de entorno:
    - SUPERUSER_EMAIL
    - SUPERUSER_PASSWORD
    - SUPERUSER_FULL_NAME

    Este superusuario puede usarse para crear otros usuarios.
    """
    from app.models.users import User

    # Verificar si ya existe algún usuario
    user_count = await User.count()
    if user_count > 0:
        print(f"Ya existen {user_count} usuarios en la base de datos. Omitiendo creación de superusuario inicial.")
        return

    # Crear el superusuario inicial
    password_helper = PasswordHelper()
    hashed_password = password_helper.hash(settings.SUPERUSER_PASSWORD)

    superuser = User(
        email=settings.SUPERUSER_EMAIL,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=True,
        full_name=settings.SUPERUSER_FULL_NAME
    )

    await superuser.insert()
