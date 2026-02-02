from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from app import schemas
from app.database import Question, Answer
from app.serializers.questionSerializers import questionEntity, questionListEntity
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.get('/')
def get_questions(limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit
    pipeline = [
        {'$match': {}},
        {'$lookup': {'from': 'answers', 'localField': 'answer_id',
                     'foreignField': '_id', 'as': 'answer'}},
        {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
        {'$skip': skip},
        {'$limit': limit}
    ]
    questions = questionListEntity(Question.aggregate(pipeline))
    return {'status': 'success', 'results': len(questions), 'questions': questions}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.CreateQuestionSchema):
    question.created_at = datetime.utcnow()
    question.updated_at = question.created_at
    
    # Convertir answer_id a ObjectId si existe
    if question.answer_id:
        question.answer_id = ObjectId(question.answer_id)
    
    try:
        result = Question.insert_one(question.dict())
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {'$lookup': {'from': 'answers', 'localField': 'answer_id',
                         'foreignField': '_id', 'as': 'answer'}},
            {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
        ]
        new_question = questionListEntity(Question.aggregate(pipeline))[0]
        return new_question
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Question with content: '{question.content}' already exists")


@router.put('/{id}')
def update_question(id: str, payload: schemas.UpdateQuestionSchema):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    
    # Convertir answer_id a ObjectId si existe en el payload
    update_data = payload.dict(exclude_none=True)
    if 'answer_id' in update_data and update_data['answer_id']:
        update_data['answer_id'] = ObjectId(update_data['answer_id'])
    
    update_data['updated_at'] = datetime.utcnow()
    
    updated_question = Question.find_one_and_update(
        {'_id': ObjectId(id)}, 
        {'$set': update_data}, 
        return_document=ReturnDocument.AFTER
    )
    
    if not updated_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No question with this id: {id} found')
    return questionEntity(updated_question)


@router.get('/{id}')
def get_question(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    pipeline = [
        {'$match': {'_id': ObjectId(id)}},
        {'$lookup': {'from': 'answers', 'localField': 'answer_id',
                     'foreignField': '_id', 'as': 'answer'}},
        {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
    ]
    db_cursor = Question.aggregate(pipeline)
    results = list(db_cursor)

    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No question with this id: {id} found")

    question = questionListEntity(results)[0]
    return question


@router.delete('/{id}')
def delete_question(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {id}")
    question = Question.find_one_and_delete({'_id': ObjectId(id)})
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No question with this id: {id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)