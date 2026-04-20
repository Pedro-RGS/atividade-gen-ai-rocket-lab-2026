from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import ClassVar

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "banco.db"

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"
    GOOGLE_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
