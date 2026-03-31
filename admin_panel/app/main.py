from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.database import init_db
from app.routers import question, answer, admin, category, csv_upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Todo lo que está antes del yield se ejecuta al arrancar
    await init_db()
    yield
    # Todo lo que está después del yield se ejecuta al cerrar (cleanup)


app = FastAPI(lifespan=lifespan)

origins = [settings.CLIENT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(question.router, tags=['Questions'], prefix='/api/questions')
app.include_router(answer.router, tags=['Answers'], prefix='/api/answers')
app.include_router(category.router, tags=['Categories'], prefix='/api/categories')
app.include_router(admin.router, tags=['Admin Panel'], prefix='/admin')
app.include_router(csv_upload.router, tags=['CSV Upload'], prefix='/admin/csv')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}