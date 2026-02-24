from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.answer import AnswerResponse


class CreateQuestionSchema(BaseModel):
    """Schema para crear una pregunta con categoría y respuesta obligatorias"""
    content: str
    category: str  # obligatorio
    answer_id: str  # obligatorio - ID de la respuesta asociada


class UpdateQuestionSchema(BaseModel):
    """Schema para actualizar una pregunta"""
    content: str 
    category: str 
    answer_id: str 

class QuestionResponse(BaseModel):
    """Pregunta serializada con su respuesta completa"""
    id: str
    content: str
    category: str
    answer: AnswerResponse  # obligatorio
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ListQuestionResponse(BaseModel):
    status: str
    results: int
    questions: List[QuestionResponse]