from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import auth_backend, fastapi_users, get_user_manager
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.models.users import User
from app.dependencies import get_superuser


router = APIRouter()

# Rutas /login y /logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

# Endpoint personalizado de registro - solo superusuarios pueden registrar
@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    superuser: User = Depends(get_superuser),
    user_manager = Depends(get_user_manager)
):
    """
    Endpoint personalizado para registrar un nuevo usuario.

    Solo los superusuarios pueden registrar nuevos usuarios en el sistema.

    Args:
        user_create: Datos del nuevo usuario (email, password, full_name).
        superuser: Usuario autenticado que debe ser superusuario.
        user_manager: Gestor de usuarios.

    Returns:
        UserRead: Información del usuario creado.

    Raises:
        HTTPException: Si el usuario actual no es superusuario (403).
        HTTPException: Si el email ya existe (400).
    """
    try:
        # Crear el usuario usando el user_manager
        user = await user_manager.create(user_create)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Rutas de usuario (get, update, delete, current user)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Password reset routes
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
    tags=["auth"],
)
