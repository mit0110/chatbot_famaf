from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import current_active_user, fastapi_users
from app.models.users import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Dependencia opcional para verificar si hay un usuario autenticado sin lanzar excepción
current_user_optional = fastapi_users.current_user(active=True, optional=True)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user: Optional[User] = Depends(current_user_optional)):
    """
    Provee la página de inicio de sesión.

    Si el usuario ya está autenticado, lo redirige a la página principal.
    """
    # Si ya está autenticado, redirigir a la página principal
    if user:
        return RedirectResponse(url="/", status_code=303)

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
