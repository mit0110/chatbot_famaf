from typing import Optional
from beanie import Document, Indexed
from typing import Annotated
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from pydantic import EmailStr, field_validator
from bson import ObjectId


class User(BeanieBaseUser, Document):
    """User model for authentication"""
    email: Annotated[EmailStr, Indexed(unique=True)]
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False

    # Additional custom fields
    full_name: Optional[str] = None

    @field_validator('id', mode='before')
    @classmethod
    def convert_id_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Settings:
        name = "users"
        email_collation = None


async def get_user_db():
    yield BeanieUserDatabase(User)
