from datetime import datetime
from fastapi import HTTPException, status, APIRouter
from app.database import Category
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

router = APIRouter()


class CategorySchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CategoryResponse(CategorySchema):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


@router.get('/')
def get_categories():
    """Get all categories"""
    categories = list(Category.find({}, {'_id': 1, 'name': 1, 'created_at': 1}).sort('created_at', 1))
    return {
        'status': 'success',
        'results': len(categories),
        'categories': [
            {'id': str(cat['_id']), 'name': cat['name'], 'created_at': cat.get('created_at')}
            for cat in categories
        ]
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
def upsert_category(category: CategorySchema):
    """Create or update a category"""
    try:
        # Try to find existing category
        existing = Category.find_one({'name': category.name})
        if existing:
            return {
                'status': 'success',
                'message': 'Category already exists',
                'id': str(existing['_id']),
                'name': existing['name']
            }
        
        # Create new category
        result = Category.insert_one({
            'name': category.name,
            'created_at': datetime.utcnow()
        })
        return {
            'status': 'success',
            'message': 'Category created',
            'id': str(result.inserted_id),
            'name': category.name
        }
    except DuplicateKeyError:
        # Shouldn't happen due to check above, but handle it
        existing = Category.find_one({'name': category.name})
        return {
            'status': 'success',
            'message': 'Category already exists',
            'id': str(existing['_id']),
            'name': existing['name']
        }
