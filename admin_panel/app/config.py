from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    CLIENT_ORIGIN: str

    model_config = {
        "env_file": "./.env",
        "extra": "ignore"  # ignora variables del .env que no están declaradas
    }


settings = Settings()