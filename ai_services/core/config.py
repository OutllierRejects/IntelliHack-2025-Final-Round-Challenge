from __future__ import annotations

"""Application configuration using Pydantic settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Environment settings for the service."""

    DATABASE_URL: str = "sqlite:///./disaster_response.db"
    DATABASE_ECHO: bool = False

    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    SUPABASE_SERVICE_ROLE_KEY: str | None = None

    JWT_SECRET: str = "disaster-response-super-secret-jwt-key-2025"
    JWT_ALGORITHM: str = "HS256"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    REDIS_URL: str = "redis://localhost:6379"

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = Field(default="gpt-4o-mini")

    # CORS Configuration
    ALLOWED_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173")

    # Agent Configuration
    AGENT_PROCESSING_INTERVAL: int = Field(default=30)
    MAX_CONCURRENT_AGENT_TASKS: int = Field(default=5)

    # Application Configuration
    APP_NAME: str = Field(default="Disaster Response Coordination System")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/app.log")

    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USERNAME: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")

    TWILIO_ACCOUNT_SID: str = Field(default="")
    TWILIO_AUTH_TOKEN: str = Field(default="")
    TWILIO_PHONE_NUMBER: str = Field(default="")

    FROM_EMAIL: str = Field(default="noreply@example.com")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()


settings = get_settings()
DATABASE_URL = settings.DATABASE_URL
DATABASE_ECHO = settings.DATABASE_ECHO
