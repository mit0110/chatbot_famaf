from datetime import datetime
from typing import List
from pydantic import BaseModel


class CreateAnswerSchema(BaseModel):
    """Schema para crear una respuesta (sin categoría, se hereda de Question)"""
    content: str


class UpdateAnswerSchema(BaseModel):
    """Schema para actualizar una respuesta"""
    content: str | None = None


class AnswerResponse(BaseModel):
    """Respuesta serializada (la categoría viene de la Question asociada)"""
    id: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ListAnswerResponse(BaseModel):
    status: str
    results: int
    answers: List[AnswerResponse]