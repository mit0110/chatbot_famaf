from fastapi import Depends, HTTPException, status
from app.auth import fastapi_users
from app.models.users import User

optional_current_user = fastapi_users.current_user(active=True, optional=True)
current_active_user = fastapi_users.current_user(active=True)

async def get_user_or_redirect(user=Depends(optional_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )
    return user


async def get_superuser(user: User = Depends(current_active_user)) -> User:
    """
    Dependencia que verifica que el usuario actual es un superusuario.

    Solo los superusuarios pueden acceder a rutas protegidas con esta dependencia.

    Args:
        user: Usuario actual autenticado.

    Returns:
        User: El usuario si es superusuario.

    Raises:
        HTTPException: Si el usuario no es un superusuario (error 403).
    """
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los superusuarios pueden acceder a este recurso"
        )
    return user