from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.routers.question import _serialize_question
from app.models.question import Question
from app.models.category import Category
from app.utils import (
    DEFAULT_CATEGORIES,
    ensure_category_exists,
    get_category_names,
    get_or_create_answer,
)
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import List, Optional
import httpx
import os
import json


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
N8N_WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://n8n:5678/") + "webhook/export-to-pinecone" 

def _serialize_for_n8n(data):
    return json.loads(json.dumps(data, default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)))


@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request, q: str = "", category: str = "", page: int = 1):
    limit = 10
    skip = (page - 1) * limit

    # Construir filtros
    filters = []
    if q:
        filters.append({
            "$or": [
                {"content": {"$regex": q, "$options": "i"}},
                {"answer.content": {"$regex": q, "$options": "i"}}
            ]
        })
    if category:
        filters.append(Question.category == category)

    total_count = await Question.find(*filters).count()
    total_pages = (total_count + limit - 1) // limit

    questions = (
        await Question.find(*filters, fetch_links=True)
        .skip(skip)
        .limit(limit)
        .sort("-created_at")
        .to_list()
    )

    category_names = await get_category_names()

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "total_items": total_count,
        "per_page": limit,
        "has_prev": page > 1,
        "has_next": page < total_pages,
    }

    return templates.TemplateResponse(
        "questions_list.html",
        {
            "request": request,
            "questions": questions,       # ahora son objetos, no dicts
            "search_query": q,
            "categories": category_names,
            "selected_category": category,
            "pagination": pagination,
        },
    )


@router.get("/create", response_class=HTMLResponse)
async def create_question_form(request: Request):
    category_names = await get_category_names()
    return templates.TemplateResponse(
        "question_form.html",
        {"request": request, "categories": category_names}
    )


@router.post("/create")
async def create_question(
    request: Request,
    content: str = Form(...),
    category: str = Form(...),
    answer_content: str = Form(...),
):
    category = await ensure_category_exists(category)
    answer = await get_or_create_answer(answer_content)

    existing = await Question.find_one(Question.content == content)
    if existing:
        # Fetchear el answer para mostrarlo en el template
        await existing.fetch_link(Question.answer)
        return templates.TemplateResponse(
            "question_duplicate.html",
            {
                "request": request,
                "message": "Una pregunta con este contenido ya existe",
                "question": existing,
            },
        )

    new_question = Question(content=content, category=category, answer=answer)
    await new_question.insert()

    return RedirectResponse(url="/admin", status_code=303)


@router.get("/edit/{question_id}", response_class=HTMLResponse)
async def edit_question_form(request: Request, question_id: PydanticObjectId):
    question = await Question.get(question_id, fetch_links=True)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verificar si la respuesta está compartida con otras preguntas
    shared_answer = False
    if question.answer and hasattr(question.answer, "id"):
        count = await Question.find(
            {"answer.$id": question.answer.id}
        ).count()
        shared_answer = count > 1

    category_names = await get_category_names()

    return templates.TemplateResponse(
        "question_edit.html",
        {
            "request": request,
            "question": question,
            "shared_answer": shared_answer,
            "categories": category_names,
        },
    )


@router.post("/edit/{question_id}")
async def update_question(
    request: Request,
    question_id: PydanticObjectId,
    content: str = Form(...),
    category: str = Form(...),
    answer_content: str = Form(...),
    update_all_answers: Optional[str] = Form(None),
):
    question = await Question.get(question_id, fetch_links=True)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    current_answer = question.answer if hasattr(question.answer, "id") else None
    old_category = question.category
    category = await ensure_category_exists(category)

    if update_all_answers == "yes" and current_answer:
        # Modificar la respuesta existente — afecta a todas las preguntas que la usan
        await current_answer.set({
            "content": answer_content,
            "updated_at": datetime.now(timezone.utc),
        })
        new_answer = current_answer
    else:
        new_answer = await get_or_create_answer(answer_content)

    question.content = content
    question.category = category
    question.answer = new_answer
    question.updated_at = datetime.now(timezone.utc)
    await question.save()

    # Limpiar answer y categoría huérfanas si cambiaron
    if current_answer and new_answer.id != current_answer.id:
        await _cleanup_orphan_answer(current_answer)
    if old_category != category:
        await _cleanup_orphan_category(old_category)

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/delete/{question_id}")
async def delete_question(question_id: PydanticObjectId):
    question = await Question.get(question_id, fetch_links=True)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await _delete_question_and_cleanup(question)

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/delete-multiple")
async def delete_multiple_questions(
    question_ids: List[PydanticObjectId] = Form(...),
):
    for question_id in question_ids:
        question = await Question.get(question_id, fetch_links=True)
        if not question:
            continue
        await _delete_question_and_cleanup(question)

    return RedirectResponse(url="/admin", status_code=303)


@router.post("/run-workflow")
async def run_workflow():
    questions = await Question.find(fetch_links=True).sort("-created_at").to_list()
    data_clean = _serialize_for_n8n({
        'status': 'success',
        'results': len(questions),
        'questions': [_serialize_question(q) for q in questions]
    })

    async with httpx.AsyncClient(timeout=600.0) as client:
        response = await client.post(N8N_WEBHOOK_URL, json=data_clean)

    if response.status_code == 404:
        return JSONResponse(status_code=503, content={
            "ok": False,
            "error": "El workflow de n8n está inactivo o el webhook no existe.",
        })

    response.raise_for_status()  # propaga cualquier otro error HTTP inesperado

    return JSONResponse(status_code=200, content={"ok": True})

async def _cleanup_orphan_answer(answer) -> None:
    """Elimina la respuesta si no está siendo usada por ninguna pregunta."""
    if not answer:
        return
    remaining = await Question.find({"answer.$id": answer.id}).count()
    if remaining == 0:
        await answer.delete()


async def _cleanup_orphan_category(category_name: str) -> None:
    """Elimina la categoría si no está siendo usada por ninguna pregunta y no es default."""
    if not category_name or category_name in DEFAULT_CATEGORIES:
        return
    remaining = await Question.find(Question.category == category_name).count()
    if remaining == 0:
        existing_category = await Category.find_one(Category.name == category_name)
        if existing_category:
            await existing_category.delete()


async def _delete_question_and_cleanup(question: Question) -> None:
    current_answer = question.answer if hasattr(question.answer, "id") else None
    question_category = question.category

    await question.delete()

    await _cleanup_orphan_answer(current_answer)
    await _cleanup_orphan_category(question_category)