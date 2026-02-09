from fastapi import APIRouter

from app.auth import auth_backend, fastapi_users
from app.schemas.users import UserCreate, UserRead, UserUpdate


router = APIRouter()

# Rutas /login y /logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

# Ruta /register para registrar un usuario
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
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
