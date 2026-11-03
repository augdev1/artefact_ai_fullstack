import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Application
    APP_NAME: str = "Empório da Música - AI Customer Support"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASE_PATH: Path = BASE_DIR / "data" / "emporio.db"

    # LLM Settings
    LLM_PROVIDER: Literal["gemini", "openai", "mock"] = "gemini"
    
    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    # OpenAI / Compatible
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str | None = None

    # Store Metadata
    STORE_NAME: str = "Empório da Música"
    STORE_CITY: str = "Campo Grande"
    STORE_STATE: str = "MS"
    STORE_ADDRESS: str = "Rua 14 de Maio, 3200 – Centro, Campo Grande - MS, 79202-333"
    STORE_PHONE: str = "(67) 3341-4444"
    STORE_WHATSAPP: str = "(67) 3321-4500"
    STORE_EMAIL: str = "contato@emporiodamusica.com.br"

settings = Settings()
