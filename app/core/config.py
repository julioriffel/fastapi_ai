from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI AI Base"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_PORT: int = 5432
    DB_ECHO: bool = False
    DATABASE_URL: str | None = None
    LOG_PATH: str = "logs/app.log"
    LOG_RETENTION: str = "10 days"
    LOG_ROTATION: str = "10 MB"

    @model_validator(mode="before")
    @classmethod
    def assemble_db_url(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data.get("DATABASE_URL"), str):
            return data
        user = data.get("POSTGRES_USER", "postgres")
        password = data.get("POSTGRES_PASSWORD", "postgres")
        server = data.get("POSTGRES_SERVER", "localhost")
        port = data.get("POSTGRES_PORT", 5432)
        db = data.get("POSTGRES_DB", "fastapi_db")
        data["DATABASE_URL"] = (
            f"postgresql+asyncpg://{user}:{password}@{server}:{port}/{db}"
        )
        return data

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
