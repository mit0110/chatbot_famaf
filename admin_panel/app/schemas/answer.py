from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator


class CreateAnswerSchema(BaseModel):
    """Schema para crear una respuesta (sin categoría, se hereda de Question)"""
    content: str

    @field_validator('content')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El contenido no puede estar vacío')
        return v.strip()


class UpdateAnswerSchema(BaseModel):
    """Schema para actualizar una respuesta"""
    content: str | None = None

    @field_validator('content')
    @classmethod
    def not_empty_if_provided(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('El contenido no puede estar vacío si se proporciona')
        return v.strip() if v else v


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