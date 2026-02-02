from datetime import datetime
from typing import List
from pydantic import BaseModel

# Answer Schemas
class AnswerBaseSchema(BaseModel):
    content: str
    category: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateAnswerSchema(AnswerBaseSchema):
    pass


class AnswerResponse(AnswerBaseSchema):
    id: str
    created_at: datetime
    updated_at: datetime


class UpdateAnswerSchema(BaseModel):
    content: str | None = None
    category: str | None = None

    class Config:
        orm_mode = True


# Question Schemas
class QuestionBaseSchema(BaseModel):
    content: str
    category: str | None = None
    answer_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CreateQuestionSchema(QuestionBaseSchema):
    pass

class QuestionResponse(QuestionBaseSchema):
    id: str
    answer: AnswerResponse | None = None
    created_at: datetime
    updated_at: datetime

class UpdateQuestionSchema(BaseModel):
    content: str | None = None
    category: str | None = None
    answer_id: str | None = None

    class Config:
        orm_mode = True


# List Responses
class ListQuestionResponse(BaseModel):
    status: str
    results: int
    questions: List[QuestionResponse]


class ListAnswerResponse(BaseModel):
    status: str
    results: int
    answers: List[AnswerResponse]