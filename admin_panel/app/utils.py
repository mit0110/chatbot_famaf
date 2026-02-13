from app.models.category import Category
from app.models.answer import Answer
from typing import List
from datetime import datetime, timezone
import re
from pymongo.errors import DuplicateKeyError

DEFAULT_CATEGORIES = [
    "Información General",
    "Cursado",
    "Exámenes",
    "Ingreso",
    "Egreso",
    "Sin Información",
]


async def get_category_names() -> List[str]:
    """
    Obtener lista de nombres de categorías ordenadas alfabéticamente.
    """
    categories = await Category.find_all().sort("+name").to_list()
    return [cat.name for cat in categories]


async def get_or_create_answer(answer_content: str, category: str) -> Answer:
    """
    Buscar una respuesta existente (case-insensitive) o crear una nueva.

    Returns:
        El documento Answer (existente o recién creado)
    """
    escaped_content = re.escape(answer_content)
    existing = await Answer.find_one({
        "content": {"$regex": f"^{escaped_content}$", "$options": "i"}
    })

    if existing:
        return existing

    new_answer = Answer(
        content=answer_content,
        category=category,
    )
    try:
        await new_answer.insert()
        return new_answer
    except DuplicateKeyError:
        # Handle race condition or regex mismatch against unique index.
        existing = await Answer.find_one({
            "content": {"$regex": f"^{escaped_content}$", "$options": "i"}
        })
        if existing:
            return existing
        raise


async def ensure_category_exists(category_name: str) -> None:
    if not category_name:
        return None

    existing = await Category.find_one({
        "name": {"$regex": f"^{re.escape(category_name)}$", "$options": "i"}
    })
    if existing:
        return existing.name

    await Category(name=category_name).insert()
    return category_name


async def normalize_category_name(category_name: str | None) -> str | None:
    if not category_name:
        return None

    existing = await Category.find_one({
        "name": {"$regex": f"^{re.escape(category_name)}$", "$options": "i"}
    })
    return existing.name if existing else category_name