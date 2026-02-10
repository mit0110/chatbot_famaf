from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.schemas.answer import AnswerResponse


class CreateQuestionSchema(BaseModel):
    content: str
    category: str | None = None
    answer_id: str | None = None  # recibís el ID en el request


class UpdateQuestionSchema(BaseModel):
    content: str | None = None
    category: str | None = None
    answer_id: str | None = None


class QuestionResponse(BaseModel):
    id: str
    content: str
    category: str | None = None
    answer: AnswerResponse | None = None  # en la response mostrás el objeto completo
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ListQuestionResponse(BaseModel):
    status: str
    results: int
    questions: List[QuestionResponse]