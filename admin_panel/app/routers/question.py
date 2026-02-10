from datetime import datetime, timezone
from fastapi import HTTPException, status, APIRouter, Response
from app.schemas.question import CreateQuestionSchema, UpdateQuestionSchema
from app.models.question import Question
from app.models.answer import Answer
from beanie import PydanticObjectId
from app.utils import ensure_category_exists

router = APIRouter()


def _serialize_question(q: Question) -> dict:
    """Helper para serializar una pregunta con su answer resuelto."""
    answer_data = None
    if q.answer and hasattr(q.answer, 'content'):  # el link fue fetcheado
        answer_data = {
            'id': str(q.answer.id),
            'content': q.answer.content,
            'category': q.answer.category,
            'created_at': q.answer.created_at,
            'updated_at': q.answer.updated_at
        }
    return {
        'id': str(q.id),
        'content': q.content,
        'category': q.category,
        'answer': answer_data,
        'created_at': q.created_at,
        'updated_at': q.updated_at
    }


@router.get('/')
async def get_questions(limit: int = 10, page: int = 1, search: str = '', category: str = ''):
    skip = (page - 1) * limit
    
    filters = []
    if search:
        filters.append({"content": {"$regex": search, "$options": "i"}})
    if category:
        filters.append(Question.category == category)
    
    query = Question.find(*filters, fetch_links=True)
    total_count = await Question.find(*filters).count()
    
    questions = await query.skip(skip).limit(limit).sort("-created_at").to_list()
    total_pages = (total_count + limit - 1) // limit
    
    return {
        'status': 'success',
        'results': len(questions),
        'questions': [_serialize_question(q) for q in questions],
        'pagination': {
            'current_page': page,
            'total_pages': total_pages,
            'total_items': total_count,
            'per_page': limit
        }
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_question(payload: CreateQuestionSchema):
    existing = await Question.find_one(Question.content == payload.content)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Question with content: '{payload.content}' already exists"
        )
    
    answer = None
    if payload.answer_id:
        answer = await Answer.get(PydanticObjectId(payload.answer_id))
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No answer with id: '{payload.answer_id}' found"
            )
    
    new_question = Question(
        content=payload.content,
        category=await ensure_category_exists(payload.category),
        answer=answer,
    )
    await new_question.insert()
    await new_question.fetch_link(Question.answer)
    
    return _serialize_question(new_question)


@router.get('/{id}')
async def get_question(id: PydanticObjectId):
    question = await Question.get(id, fetch_links=True)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No question with this id: {id} found"
        )
    return _serialize_question(question)


@router.put('/{id}')
async def update_question(id: PydanticObjectId, payload: UpdateQuestionSchema):
    question = await Question.get(id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No question with this id: {id} found'
        )
    
    update_data = payload.model_dump(exclude_none=True)

    if 'category' in update_data:
        update_data['category'] = await ensure_category_exists(
            update_data['category']
        )
    
    # Resolver answer_id a un Link si viene en el payload
    if 'answer_id' in update_data:
        answer = await Answer.get(PydanticObjectId(update_data.pop('answer_id')))
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Answer not found"
            )
        question.answer = answer

    update_data['updated_at'] = datetime.now(timezone.utc)
    
    # set() para los campos simples, save() para persistir el link
    await question.set({k: v for k, v in update_data.items()})
    await question.save()
    await question.fetch_link(Question.answer)
    
    return _serialize_question(question)


@router.delete('/{id}')
async def delete_question(id: PydanticObjectId):
    question = await Question.get(id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No question with this id: {id} found'
        )
    await question.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)