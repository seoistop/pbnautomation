from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"), env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "PBN Automation API"
    API_TOKEN: str
    DATABASE_URL: str = "sqlite:///./pbn.db"
    FERNET_KEY: str
    GOOGLE_SHEET_ID: str | None = None
    GOOGLE_SERVICE_ACCOUNT_JSON: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
