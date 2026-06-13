from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "BizGro"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://bizgro:bizgro_secret@localhost:5432/bizgro"
    redis_url: str = "redis://localhost:6379"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    secret_key: str = "dev_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
