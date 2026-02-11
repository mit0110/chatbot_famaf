from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.models.users import User
from app.routers import auth, pages, question, answer, admin, category
from app.database import init_db
from app.auth import current_active_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar base de datos
    await init_db()
    yield
    # Agregar código que desee ejecutarse después de que se finalize el sv


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
app.include_router(auth.router, tags=['Authentication'], prefix='/auth')
app.include_router(pages.router, tags=['Pages'])


# Manejador de excepciones para redirigir a login si el usuario no está autenticado
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manejador personalizado de excepciones HTTP.

    Redirige a la página de login si el usuario intenta acceder a una ruta
    protegida sin estar autenticado (HTTP 401 - Unauthorized o 403 - Forbidden).

    Args:
        request (Request): La solicitud HTTP actual.
        exc (HTTPException): La excepción levantada.

    Returns:
        RedirectResponse: Redirige a /login si es 401 o 403, sino lanza la excepción.
    """
    if exc.status_code in [401, 403]:
        return RedirectResponse(url="/login", status_code=303)
    raise exc


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}