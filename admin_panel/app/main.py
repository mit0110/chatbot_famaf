from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import question, answer

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question.router, tags=['Questions'], prefix='/api/questions')
app.include_router(answer.router, tags=['Answers'], prefix='/api/answers')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
