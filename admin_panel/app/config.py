from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    JWT_PUBLIC_KEY: str = "your-public-key"
    JWT_PRIVATE_KEY: str = "your-private-key"
    REFRESH_TOKEN_EXPIRES_IN: int = 604800  # 7 days
    ACCESS_TOKEN_EXPIRES_IN: int = 3600  # 1 hour
    JWT_ALGORITHM: str = "HS256"

    # Secret key for FastAPI Users authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'
        extra = "ignore"  # Ignore extra fields from .env


settings = Settings()
