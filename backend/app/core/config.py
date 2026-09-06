import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="allow")

    PROJECT_NAME: str = "WhatsApp Sales AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "production-secret-key-whatsapp-sales-ai-enterprise-grade-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    # Local fallback to async SQLite for development/testing if PostgreSQL is not active
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite+aiosqlite:///./whatsapp_sales_ai.db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # AI / LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "mock-openai-key")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # WhatsApp Business Cloud API Defaults
    WHATSAPP_API_VERSION: str = "v20.0"
    WHATSAPP_API_URL: str = "https://graph.facebook.com"
    WHATSAPP_DEFAULT_VERIFY_TOKEN: str = "sales_ai_webhook_verify_secret"
    WHATSAPP_APP_SECRET: str = os.getenv("WHATSAPP_APP_SECRET", "mock_app_secret_for_signature_validation")

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]


settings = Settings()
