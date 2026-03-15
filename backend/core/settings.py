from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    APP_NAME: str = "Smart GRH"
    DEBUG: bool = False
    DATABASE_URL: str
    CREATE_TABLES_ON_STARTUP: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Use the Pydantic v2 settings configuration API.
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
