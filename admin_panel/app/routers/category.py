from datetime import datetime, timezone
from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from beanie.exceptions import RevisionIdWasChanged
from app.models.category import Category

router = APIRouter()


class CategorySchema(BaseModel):
    name: str


@router.get('/')
async def get_categories():
    categories = await Category.find_all().sort("+created_at").to_list()
    return {
        'status': 'success',
        'results': len(categories),
        'categories': [
            {'id': str(cat.id), 'name': cat.name, 'created_at': cat.created_at}
            for cat in categories
        ]
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def upsert_category(payload: CategorySchema):
    existing = await Category.find_one(Category.name == payload.name)
    if existing:
        return {
            'status': 'success',
            'message': 'Category already exists',
            'id': str(existing.id),
            'name': existing.name
        }
    
    try:
        new_cat = await Category(name=payload.name).insert()
        return {
            'status': 'success',
            'message': 'Category created',
            'id': str(new_cat.id),
            'name': new_cat.name
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{payload.name}' already exists"
        )