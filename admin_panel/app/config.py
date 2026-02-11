from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde las variables de entorno.

    Esta clase gestiona todas las variables de configuración de la aplicación,
    incluyendo la conexión a la base de datos.
    Las valores se cargan desde el archivo .env en el directorio raíz.

    Args:
        DATABASE_URL (str): URL de conexión a MongoDB.
        MONGO_INITDB_DATABASE (str): Nombre de la base de datos MongoDB.
        ACCESS_TOKEN_EXPIRES_IN (int): Tiempo de expiración de la cookie de sesión en segundos (por defecto: 3600 = 1 hora).
        SECRET_KEY (str): Clave secreta para la autenticación JWT.
        CLIENT_ORIGIN (str): Origen permitido para CORS (URL del cliente).
    """
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str

    ACCESS_TOKEN_EXPIRES_IN: int = 3600

    # Clave secreta para la autenticación usando FastAPI Users
    SECRET_KEY: str

    CLIENT_ORIGIN: str
    class Config:
        env_file = './.env'
        extra = "ignore"  # ignorar campos extra del .env


settings = Settings()