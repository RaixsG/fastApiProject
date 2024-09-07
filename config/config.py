import os
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# APP_DIR = Path(__file__).parent.parent / "app"

class Settings(BaseSettings):
    PROJECT_DIR: os.PathLike[str] = Path(__file__).parent.parent
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_USERNAME: str = os.getenv("DB_USERNAME")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    secret_key: str | None = os.getenv("SECRET_KEY")
    algorithm: str | None = os.getenv("ALGORITHM")
    access_token_expire_minutes: int | None = None

    class Config:
        env_prefix = ""
        env_file_encoding = "utf-8"
        # env_file = f"{APP_DIR}/.env"
        env_file = ".env"
        extra="allow"


settings = Settings()