from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database import Question, Answer, Category
from bson.objectid import ObjectId
from datetime import datetime
from typing import Optional
from pymongo.errors import DuplicateKeyError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request):
    """Página principal del admin - lista de preguntas"""
    pipeline = [
        {'$lookup': {
            'from': 'answers',
            'localField': 'answer_id',
            'foreignField': '_id',
            'as': 'answer'
        }},
        {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
        {'$sort': {'created_at': -1}}
    ]
    questions = list(Question.aggregate(pipeline))
    
    return templates.TemplateResponse(
        "questions_list.html",
        {"request": request, "questions": questions}
    )


@router.get("/search", response_class=HTMLResponse)
async def search_questions(request: Request, q: str = ""):
    """Buscar preguntas por contenido"""
    if q:
        pipeline = [
            {'$match': {
                'content': {'$regex': q, '$options': 'i'}
            }},
            {'$lookup': {
                'from': 'answers',
                'localField': 'answer_id',
                'foreignField': '_id',
                'as': 'answer'
            }},
            {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
            {'$sort': {'created_at': -1}}
        ]
    else:
        pipeline = [
            {'$lookup': {
                'from': 'answers',
                'localField': 'answer_id',
                'foreignField': '_id',
                'as': 'answer'
            }},
            {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}},
            {'$sort': {'created_at': -1}}
        ]
    
    questions = list(Question.aggregate(pipeline))
    
    return templates.TemplateResponse(
        "questions_list.html",
        {"request": request, "questions": questions, "search_query": q}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_question_form(request: Request):
    """Formulario para crear pregunta"""
    categories = list(Category.find({}, {'_id': 0, 'name': 1}).sort('name', 1))
    category_names = [cat['name'] for cat in categories]
    return templates.TemplateResponse(
        "question_form.html",
        {"request": request, "categories": category_names}
    )


@router.post("/create")
async def create_question(
    request: Request,
    content: str = Form(...),
    category: str = Form(...),
    answer_content: str = Form(...)
):
    """Crear pregunta con respuesta"""
    
    # Buscar si ya existe una respuesta con ese contenido
    existing_answer = Answer.find_one({
        'content': {'$regex': f'^{answer_content}$', '$options': 'i'}
    })
    
    if existing_answer:
        # Usar respuesta existente
        answer_id = existing_answer['_id']
    else:
        # Crear nueva respuesta
        new_answer = {
            'content': answer_content,
            'category': category,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = Answer.insert_one(new_answer)
        answer_id = result.inserted_id
    
    # Crear pregunta
    new_question = {
        'content': content,
        'category': category,
        'answer_id': answer_id,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    try:
        Question.insert_one(new_question)
        return RedirectResponse(url="/admin", status_code=303)
    except DuplicateKeyError:
        # Encontrar la pregunta duplicada
        existing_question = Question.find_one({'content': content})
        
        # Obtener la respuesta asociada
        pipeline = [
            {'$match': {'_id': existing_question['_id']}},
            {'$lookup': {
                'from': 'answers',
                'localField': 'answer_id',
                'foreignField': '_id',
                'as': 'answer'
            }},
            {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}}
        ]
        
        results = list(Question.aggregate(pipeline))
        question_with_answer = results[0] if results else existing_question
        
        return templates.TemplateResponse(
            "question_duplicate.html",
            {
                "request": request,
                "error": True,
                "message": "Una pregunta con este contenido ya existe",
                "question": question_with_answer
            }
        )


@router.get("/edit/{question_id}", response_class=HTMLResponse)
async def edit_question_form(request: Request, question_id: str):
    """Formulario para editar pregunta"""
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    pipeline = [
        {'$match': {'_id': ObjectId(question_id)}},
        {'$lookup': {
            'from': 'answers',
            'localField': 'answer_id',
            'foreignField': '_id',
            'as': 'answer'
        }},
        {'$unwind': {'path': '$answer', 'preserveNullAndEmptyArrays': True}}
    ]
    
    results = list(Question.aggregate(pipeline))
    if not results:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question = results[0]
    
    # Verificar si la respuesta está asociada a otras preguntas
    answer_id = question.get('answer_id')
    shared_answer = False
    
    if answer_id:
        count = Question.count_documents({'answer_id': answer_id})
        shared_answer = count > 1
    
    # Obtener categorías
    categories = list(Category.find({}, {'_id': 0, 'name': 1}).sort('name', 1))
    category_names = [cat['name'] for cat in categories]
    
    return templates.TemplateResponse(
        "question_edit.html",
        {
            "request": request,
            "question": question,
            "shared_answer": shared_answer,
            "categories": category_names
        }
    )


@router.post("/edit/{question_id}")
async def update_question(
    request: Request,
    question_id: str,
    content: str = Form(...),
    category: str = Form(...),
    answer_content: str = Form(...),
    update_all_answers: Optional[str] = Form(None)
):
    """Actualizar pregunta y respuesta"""
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    question = Question.find_one({'_id': ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Obtener la respuesta actual
    current_answer_id = question.get('answer_id')
    
    if update_all_answers == "yes" and current_answer_id:
        # Actualizar la respuesta existente (afecta a todas las preguntas)
        Answer.update_one(
            {'_id': current_answer_id},
            {'$set': {
                'content': answer_content,
                'category': category,
                'updated_at': datetime.utcnow()
            }}
        )
        new_answer_id = current_answer_id
    else:
        # Buscar si ya existe una respuesta con ese contenido
        existing_answer = Answer.find_one({
            'content': {'$regex': f'^{answer_content}$', '$options': 'i'}
        })
        
        if existing_answer:
            # Usar respuesta existente
            new_answer_id = existing_answer['_id']
        else:
            # Crear nueva respuesta
            new_answer = {
                'content': answer_content,
                'category': category,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = Answer.insert_one(new_answer)
            new_answer_id = result.inserted_id
    
    # Actualizar pregunta
    Question.update_one(
        {'_id': ObjectId(question_id)},
        {'$set': {
            'content': content,
            'category': category,
            'answer_id': new_answer_id,
            'updated_at': datetime.utcnow()
        }}
    )
    
    # Si se cambió la respuesta y hay una anterior, verificar si la anterior debe ser eliminada
    if new_answer_id != current_answer_id and current_answer_id:
        # Asegurar que current_answer_id es un ObjectId válido
        if isinstance(current_answer_id, str):
            current_answer_id = ObjectId(current_answer_id)
        
        # Contar cuántas preguntas usan la respuesta anterior
        count = Question.count_documents({'answer_id': current_answer_id})
        if count == 0:
            # Si nadie más usa esa respuesta, eliminarla
            Answer.delete_one({'_id': current_answer_id})
    
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/delete/{question_id}")
async def delete_question(question_id: str):
    """Eliminar pregunta y respuesta si no está asociada a otras"""
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    question = Question.find_one({'_id': ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Obtener answer_id
    answer_id = question.get('answer_id')
    
    # Eliminar pregunta
    Question.delete_one({'_id': ObjectId(question_id)})
    
    # Si la respuesta no está asociada a ninguna otra pregunta, eliminarla
    if answer_id:
        # Asegurar que answer_id es un ObjectId válido
        if isinstance(answer_id, str):
            answer_id = ObjectId(answer_id)
        
        count = Question.count_documents({'answer_id': answer_id})
        if count == 0:
            Answer.delete_one({'_id': answer_id})
    
    return RedirectResponse(url="/admin", status_code=303)