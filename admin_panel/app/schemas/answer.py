from datetime import datetime
from typing import List
from pydantic import BaseModel


class CreateAnswerSchema(BaseModel):
    content: str
    category: str | None = None


class UpdateAnswerSchema(BaseModel):
    content: str | None = None
    category: str | None = None


class AnswerResponse(BaseModel):
    id: str
    content: str
    category: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # orm_mode en Pydantic v2


class ListAnswerResponse(BaseModel):
    status: str
    results: int
    answers: List[AnswerResponse]