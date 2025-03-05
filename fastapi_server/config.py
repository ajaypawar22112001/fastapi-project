import os
from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # Required settings
    PG_DATABASE_URL: str
    # JWT_SECRET_KEY: str
    # JWT_ALGORITHM: str
    # JWT_EXPIRATION_MINUTES: int
    # MAGIC_LINK_EXPIRATION_MINUTES: int

    # Optional settings
    ENVIRONMENT: str = Environment.PRODUCTION.value
    ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings():
    return Settings()
