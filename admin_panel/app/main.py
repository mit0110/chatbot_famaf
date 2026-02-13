from typing import Optional
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.config import settings
from app.dependencies import get_user_or_redirect
from app.models.users import User
from app.routers import auth, question, answer, admin, category, login
from app.database import init_db
from app.auth import current_active_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar base de datos
    await init_db()
    yield
    # Agregar código que desee ejecutarse después de que se finalize el sv


app = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None, redoc_url=None)

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
app.include_router(auth.router, tags=['Authentication'], prefix='/auth')
app.include_router(login.router, tags=['Login'])


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}


@app.get("/docs", include_in_schema=False)
async def get_documentation(_: Optional[User] = Depends(get_user_or_redirect)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Admin Panel - Chatbot FAMAF")

@app.get("/openapi.json", include_in_schema=False)
async def openapi(_: Optional[User] = Depends(current_active_user)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)