from pydantic_settings import BaseSettings
from sqlalchemy import URL
import secrets
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: URL = URL.create(
        drivername="postgresql+asyncpg", username="postgres", password="qwerty",host="localhost", port=5432,
        database="postgres"

    )
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    FIRST_SUPERUSER: str = "qwerty"
    FIRST_SUPERUSER_PASS: str = "qweqwe"
    BASE_DIR: Path = Path(__file__).resolve().parent
    MEDIA_URL: str = "media"
    MEDIA_ROOT: Path = BASE_DIR / MEDIA_URL
    STATIC_URL: str = "static"
    STATIC_ROOT: Path = BASE_DIR / STATIC_URL
    HOST: str = "localhost:8000"
    PROTO: str = "http"
    LOG_LEVEL: str = "DEBUG"

settings = Settings()
