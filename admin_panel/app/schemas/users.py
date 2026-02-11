"""
Esquemas Pydantic para validación de datos de usuario.

Este módulo contiene los esquemas Pydantic utilizados para validar
los datos de entrada y salida en las operaciones relacionadas con usuarios.
Extiende los esquemas base de FastAPI Users para proporcionar validaciones
personalizadas.
"""


from typing import Optional
from fastapi_users import schemas
from pydantic import field_validator
from bson import ObjectId


class UserRead(schemas.BaseUser[str]):
    """
    Esquema para leer/devolver información de usuario.

    Este esquema se utiliza cuando se devuelve información del usuario
    a través de la API. Incluye todos los campos públicos del usuario.

    Atributos:
        id (str): Identificador único del usuario.
        email (EmailStr): Correo electrónico del usuario.
        is_active (bool): Si la cuenta del usuario está activa.
        full_name (Optional[str]): Nombre completo del usuario (opcional).
    """
    full_name: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def convert_objectid_to_str(cls, v):
        """
        Convierte ObjectId de MongoDB a string.

        Asegura que el ID de usuario sea compatible con JSON al convertir
        los ObjectIds de BSON a representación de string.

        Args:
            v: El valor a convertir (puede ser ObjectId o string).

        Returns:
            str: El ID convertido a string.
        """
        if isinstance(v, ObjectId):
            return str(v)
        return v


class UserCreate(schemas.BaseUserCreate):
    """
    Esquema para crear un nuevo usuario.

    Utilizado en el endpoint de registro para validar los datos
    proporcionados por el usuario al crear una nueva cuenta.

    Atributos:
        email (EmailStr): Correo electrónico único del nuevo usuario.
        password (str): Contraseña del usuario (mínimo 8 caracteres).
        full_name (Optional[str]): Nombre completo del usuario (opcional).
    """
    full_name: Optional[str] = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """
        Valida que la contraseña cumple con los requisitos de seguridad.

        Verifica que la contraseña tenga una longitud mínima de 8 caracteres.

        Args:
            v (str): La contraseña a validar.

        Returns:
            str: La contraseña validada.

        Raises:
            ValueError: Si la contraseña tiene menos de 8 caracteres.
        """
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v


class UserUpdate(schemas.BaseUserUpdate):
    """
    Esquema para actualizar información de un usuario.

    Utilizado en el endpoint de actualización de perfil para validar
    los datos proporcionados por el usuario al modificar su información.

    Atributos:
        email (EmailStr, Optional): Nuevo correo electrónico (opcional).
        password (str, Optional): Nueva contraseña (opcional).
        full_name (Optional[str]): Nuevo nombre completo (opcional).
    """
    full_name: Optional[str] = None
