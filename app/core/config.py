from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str  # формат: postgresql+asyncpg://user:pass@db:5432/dbname
    ENV: str = "dev"   # dev/prod
    API_V1_PREFIX: str = "/api/v1"


settings = Settings()