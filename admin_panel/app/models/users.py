"""
Modelos de usuario para autenticación y gestión de usuarios.

Este módulo contiene la definición del modelo de Usuario que se utiliza
para almacenar y gestionar la información de usuarios en la aplicación.
Utiliza Beanie como ODM para MongoDB y FastAPI Users para autenticación.
"""

from typing import Optional
from beanie import Document, Indexed
from typing import Annotated
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from pydantic import EmailStr, field_validator
from bson import ObjectId


class User(BeanieBaseUser, Document):
    """
    Modelo de usuario para autenticación y gestión de sesiones.

    Extiende BeanieBaseUser de FastAPI Users y Document de Beanie para
    proporcionar funcionalidades de autenticación integradas con MongoDB.

    Atributos:
        id (str): Identificador único generado automáticamente por MongoDB.
        email (EmailStr): Correo electrónico único del usuario.
        hashed_password (str): Contraseña hasheada de forma segura con bcrypt.
        is_active (bool): Indica si la cuenta del usuario está activa (por defecto: True).
        full_name (Optional[str]): Nombre completo del usuario (opcional).
    """
    email: Annotated[EmailStr, Indexed(unique=True)]
    hashed_password: str
    is_active: bool = True

    # Campos personalizados adicionales
    full_name: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def convert_id_to_str(cls, v):
        """
        Convierte el ObjectId de MongoDB a string.

        Este validador asegura que el ID de usuario sea compatible con JSON
        al convertir los ObjectIds de BSON a strings.

        Args:
            v: El valor a validar (puede ser ObjectId o string).

        Returns:
            str: El ID convertido a string.
        """
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Settings:
        """Configuración de Beanie para la colección de usuarios."""
        name = "users"  # Nombre de la colección en MongoDB
        email_collation = None  # Comparaciones de email case-sensitive


async def get_user_db():
    """
    Dependencia asincrónica para acceder a la base de datos de usuarios.

    Esta función proporciona una instancia de BeanieUserDatabase que puede
    inyectarse en rutas protegidas para acceder a los datos de usuarios.

    Yields:
        BeanieUserDatabase[User, str]: Gestor de base de datos de usuarios.
    
    Ejemplo:
        >>> from fastapi import Depends
        >>> async def protected_route(user_db = Depends(get_user_db)):
        ...     pass
    """
    yield BeanieUserDatabase(User)
