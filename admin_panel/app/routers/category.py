from fastapi import HTTPException, status, APIRouter
from pydantic import BaseModel
from app.models.category import Category
from app.utils import normalize_category_name

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
    canonical_name = await normalize_category_name(payload.name)
    existing = await Category.find_one(Category.name == canonical_name)
    if existing:
        return {
            'status': 'success',
            'message': 'Category already exists',
            'id': str(existing.id),
            'name': existing.name
        }
    
    try:
        new_cat = await Category(name=canonical_name).insert()
        return {
            'status': 'success',
            'message': 'Category created',
            'id': str(new_cat.id),
            'name': new_cat.name
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{canonical_name}' already exists"
        )