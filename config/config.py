from pydantic_settings import BaseSettings
import os
from pathlib import Path

# APP_DIR = Path(__file__).parent.parent / "app"

class Settings(BaseSettings):
    PROJECT_DIR: os.PathLike[str] = Path(__file__).parent.parent
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    secret_key: str | None = None
    algorithm: str | None = None
    access_token_expire_minutes: int | None = None

    class Config:
        env_prefix = ""
        env_file_encoding = "utf-8"
        # env_file = f"{APP_DIR}/.env"
        env_file = ".env"
        extra="allow"


settings = Settings()