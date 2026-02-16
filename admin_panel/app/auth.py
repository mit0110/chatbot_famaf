"""
Configuración de autenticación con FastAPI Users.

Este módulo configura todo el sistema de autenticación de la aplicación,
incluyendo la gestión de usuarios, estrategias JWT, transporte de cookies
y dependencias para rutas protegidas.
"""

from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase

from app.models.users import User, get_user_db
from app.config import settings




class UserManager(BaseUserManager[User, str]):
    """
    Gestor de usuarios para manejar operaciones relacionadas con usuarios.

    Extiende BaseUserManager de FastAPI Users para proporcionar funcionalidades
    personalizadas de gestión de usuarios incluyendo registro y verificación
    de correo electrónico.

    Atributos:
        verification_token_secret (str): Clave secreta para tokens de verificación.
    """
    verification_token_secret = settings.SECRET_KEY

    def parse_id(self, value: str) -> str:
        """
        Convierte el ID de usuario desde su representación en el token a su forma interna.

        Como utilizamos strings como ID, no se requiere conversión adicional.

        Args:
            value (str): El ID del usuario como string.

        Returns:
            str: El ID sin cambios.
        """
        return value

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Callback ejecutado después de que un usuario se registra exitosamente.

        Actualmente registra el evento en la consola. Puede extenderse para
        enviar correos de bienvenida, crear recursos relacionados, etc.

        Args:
            user (User): El usuario recién registrado.
            request (Optional[Request]): La solicitud HTTP actual.
        """
        print(f"User {user.id} has registered.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        Callback ejecutado cuando se solicita verificación de correo.

        Actualmente registra el token en la consola. En producción, debería
        enviarse por correo electrónico al usuario.

        Args:
            user (User): El usuario que solicita verificación.
            token (str): Token de verificación único.
            request (Optional[Request]): La solicitud HTTP actual.
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    """
    Dependencia asincrónica que proporciona la instancia del gestor de usuarios.

    Esta función actúa como una dependencia inyectable que proporciona acceso
    al UserManager en las rutas y otros servicios.

    Args:
        user_db (BeanieUserDatabase): Base de datos de usuarios inyectada.

    Yields:
        UserManager: La instancia del gestor de usuarios.
    """
    yield UserManager(user_db)


# Configuración del transporte de autenticación por cookies
cookie_transport = CookieTransport(
    cookie_name="adminuserauth",  # Nombre de la cookie
    cookie_max_age=settings.ACCESS_TOKEN_EXPIRES_IN,  # Tiempo de vida de la cookie
    cookie_path="/",  # Ruta válida para la cookie
    cookie_secure=False  # TODO: Cambiar a True en producción (requiere HTTPS)
)


def get_jwt_strategy() -> JWTStrategy:
    """
    Proporciona la estrategia JWT para la autenticación.

    Configura los parámetros de JWT incluyendo la clave secreta
    y el tiempo de expiración de los tokens.

    Returns:
        JWTStrategy: Estrategia configurada para tokens JWT.
    """
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_EXPIRES_IN)


# Backend de autenticación configurado
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


# Instancia principal de FastAPI Users
fastapi_users = FastAPIUsers[User, str](
    get_user_manager,
    [auth_backend],
)


# Dependencias para rutas protegidas
current_active_user = fastapi_users.current_user(active=True)
"""
Dependencia que verifica que el usuario actual está autenticado y activo.

Uso en las rutas para requerir autenticación:

    @router.get("/protegido")
    async def ruta_protegida(user: User = Depends(current_active_user)):
        return {"message": f"Hola {user.email}"}
"""

