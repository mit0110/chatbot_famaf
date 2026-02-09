from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user
from app.models.users import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Provee la página de inicio de sesión"""
    return templates.TemplateResponse(name="login.html", request=request)


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request, user: User = Depends(current_active_user)):
    """
    Página de inicio protegida.

    Solo se puede acceder si el usuario está autenticado y activo.
    Si no está autenticado, redirige al login automáticamente.
    Muestra información del usuario actual.
    """
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request, "user": user}
    )
