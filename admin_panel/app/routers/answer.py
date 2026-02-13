from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status, APIRouter, Response
from app.schemas.answer import CreateAnswerSchema, UpdateAnswerSchema
from app.models.answer import Answer
from beanie import PydanticObjectId
from app.auth import current_active_user
from app.utils import ensure_category_exists

router = APIRouter(
    dependencies=[Depends(current_active_user)]
)


@router.get('/')
async def get_answers(limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    
    query = Answer.find_all()
    if search:
        query = Answer.find({"content": {"$regex": search, "$options": "i"}})
    
    answers = await query.skip(skip).limit(limit).to_list()
    
    return {
        'status': 'success',
        'results': len(answers),
        'answers': [
            {
                'id': str(a.id),
                'content': a.content,
                'category': a.category,
                'created_at': a.created_at,
                'updated_at': a.updated_at
            }
            for a in answers
        ]
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_answer(payload: CreateAnswerSchema):
    existing = await Answer.find_one(Answer.content == payload.content)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answer already exists"
        )

    category = await ensure_category_exists(payload.category)
    
    new_answer = Answer(
        content=payload.content,
        category=category,
    )
    await new_answer.insert()
    
    return {
        'id': str(new_answer.id),
        'content': new_answer.content,
        'category': new_answer.category,
        'created_at': new_answer.created_at,
        'updated_at': new_answer.updated_at
    }


@router.put('/{id}')
async def update_answer(id: PydanticObjectId, payload: UpdateAnswerSchema):
    answer = await Answer.get(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No answer with this id: {id} found'
        )
    
    update_data = payload.model_dump(exclude_none=True)
    if 'category' in update_data:
        update_data['category'] = await ensure_category_exists(
            update_data['category']
        )
    update_data['updated_at'] = datetime.now(timezone.utc)
    
    await answer.set(update_data)
    
    return {
        'id': str(answer.id),
        'content': answer.content,
        'category': answer.category,
        'created_at': answer.created_at,
        'updated_at': answer.updated_at
    }


@router.get('/{id}')
async def get_answer(id: PydanticObjectId):
    answer = await Answer.get(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No answer with this id: {id} found"
        )
    return {
        'id': str(answer.id),
        'content': answer.content,
        'category': answer.category,
        'created_at': answer.created_at,
        'updated_at': answer.updated_at
    }


@router.delete('/{id}')
async def delete_answer(id: PydanticObjectId):
    answer = await Answer.get(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No answer with this id: {id} found'
        )
    await answer.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)