from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Answer
from app.serializers.answerSerializers import answerEntity, answerListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.get('/')
def get_answers(limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$skip': skip},
        {'$limit': limit}
    ]
    answers = answerListEntity(Answer.aggregate(pipeline))
    return {'status': 'success', 'results': len(answers), 'answers': answers}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_answer(answer: schemas.CreateAnswerSchema):
    answer.created_at = datetime.utcnow()
    answer.updated_at = answer.created_at
    
    try:
        result = Answer.insert_one(answer.dict())
        new_answer = answerEntity(Answer.find_one({'_id': result.inserted_id}))
        return new_answer
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Answer already exists")


@router.put('/{id}')
def update_answer(id: str, payload: schemas.UpdateAnswerSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    
    update_data = payload.dict(exclude_none=True)
    update_data['updated_at'] = datetime.utcnow()
    
    updated_answer = Answer.find_one_and_update(
        {'_id': ObjectId(id)}, 
        {'$set': update_data}, 
        return_document=ReturnDocument.AFTER
    )
    
    if not updated_answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No answer with this id: {id} found')
    return answerEntity(updated_answer)


@router.get('/{id}')
def get_answer(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    answer = answerEntity(Answer.find_one({'_id': ObjectId(id)}))

    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No answer with this id: {id} found")
    return answer


@router.delete('/{id}')
def delete_answer(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    answer = Answer.find_one_and_delete({'_id': ObjectId(id)})
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No answer with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)