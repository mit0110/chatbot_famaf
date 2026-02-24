from datetime import datetime, timezone
from fastapi import HTTPException, status, APIRouter, Response
from app.schemas.answer import CreateAnswerSchema, UpdateAnswerSchema
from app.models.answer import Answer
from beanie import PydanticObjectId

router = APIRouter()


def _serialize_answer(a: Answer) -> dict:
    """Helper para serializar una respuesta."""
    return {
        'id': str(a.id),
        'content': a.content,
        'created_at': a.created_at,
        'updated_at': a.updated_at
    }


@router.get('/')
async def get_answers(limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    
    if search:
        query = Answer.find({"content": {"$regex": search, "$options": "i"}})
    else:
        query = Answer.find_all()
    
    answers = await query.skip(skip).limit(limit).to_list()
    
    return {
        'status': 'success',
        'results': len(answers),
        'answers': [_serialize_answer(a) for a in answers]
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_answer(payload: CreateAnswerSchema):
    existing = await Answer.find_one(Answer.content == payload.content)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answer already exists"
        )
    
    new_answer = Answer(content=payload.content)
    await new_answer.insert()
    
    return _serialize_answer(new_answer)


@router.put('/{id}')
async def update_answer(id: PydanticObjectId, payload: UpdateAnswerSchema):
    answer = await Answer.get(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No answer with this id: {id} found'
        )
    
    update_data = payload.model_dump(exclude_none=True)
    update_data['updated_at'] = datetime.now(timezone.utc)
    
    await answer.set(update_data)
    
    return _serialize_answer(answer)


@router.get('/{id}')
async def get_answer(id: PydanticObjectId):
    answer = await Answer.get(id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No answer with this id: {id} found"
        )
    return _serialize_answer(answer)


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