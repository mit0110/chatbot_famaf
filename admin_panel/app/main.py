from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.routers import auth, pages
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar la Base de Datos
    await init_db()
    yield
    # Al apagar el servidor


app = FastAPI(lifespan=lifespan)

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

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")


# TODO: Migrate these routers to Beanie models
# app.include_router(question.router, tags=['Questions'], prefix='/api/questions')
# app.include_router(answer.router, tags=['Answers'], prefix='/api/answers')
# app.include_router(admin.router, tags=['Admin Panel'], prefix='/admin')
# app.include_router(category.router, tags=['Categories'], prefix='/api/categories')

app.include_router(auth.router, tags=['Authentication'], prefix='/auth')
app.include_router(pages.router, tags=['Pages'])

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
