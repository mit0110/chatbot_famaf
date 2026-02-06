from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr, Field, field_validator
from bson import ObjectId


class UserRead(schemas.BaseUser[str]):
    """Schema for reading user data"""
    full_name: Optional[str] = None
    
    class Config:
        # Exclude is_superuser from the schema
        fields = {'is_superuser': {'exclude': True}}

    @field_validator('id', mode='before')
    @classmethod
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a user"""
    full_name: Optional[str] = None
    
    class Config:
        # Exclude is_superuser from the schema
        fields = {'is_superuser': {'exclude': True}}


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating a user"""
    full_name: Optional[str] = None
    
    class Config:
        # Exclude is_superuser from the schema
        fields = {'is_superuser': {'exclude': True}}
