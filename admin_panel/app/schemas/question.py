from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator
from app.schemas.answer import AnswerResponse


class CreateQuestionSchema(BaseModel):
    """Schema para crear una pregunta con categoría y respuesta obligatorias"""
    content: str
    category: str  # obligatorio
    answer_id: str  # obligatorio - ID de la respuesta asociada

    @field_validator('content', 'category', 'answer_id')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Este campo no puede estar vacío')
        return v.strip()


class UpdateQuestionSchema(BaseModel):
    """Schema para actualizar una pregunta - todos los campos opcionales"""
    content: str | None = None
    category: str | None = None
    answer_id: str | None = None

    @field_validator('content', 'category', 'answer_id')
    @classmethod
    def not_empty_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('Este campo no puede estar vacío si se proporciona')
        return v.strip() if v else v

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