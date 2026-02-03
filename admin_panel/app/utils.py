from app.database import Category, Answer
from typing import Optional, List
from datetime import datetime
from bson.objectid import ObjectId

def get_category_names() -> List[str]:
    """
    Obtener lista de nombres de categorías ordenadas alfabéticamente.
    
    Returns:
        Lista de strings con los nombres de las categorías
    """
    categories = list(Category.find({}, {'_id': 0, 'name': 1}).sort('name', 1))
    return [cat['name'] for cat in categories]

def get_or_create_answer(answer_content: str, category: str) -> ObjectId:
    """
    Buscar una respuesta existente o crear una nueva.
    
    Args:
        answer_content: Contenido de la respuesta
        category: Categoría de la respuesta
        
    Returns:
        ObjectId de la respuesta (existente o recién creada)
    """
    existing_answer = Answer.find_one({
        'content': {'$regex': f'^{answer_content}$', '$options': 'i'}
    })
    
    if existing_answer:
        # Usar respuesta existente
        return existing_answer['_id']
    else:
        # Crear nueva respuesta
        new_answer = {
            'content': answer_content,
            'category': category,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = Answer.insert_one(new_answer)
        return result.inserted_id