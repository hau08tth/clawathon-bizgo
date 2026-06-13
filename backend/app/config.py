from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "BizGro"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "sqlite+aiosqlite:///./bizgro.db"
    redis_url: str = "redis://localhost:6379"

    llm_api_key: str = ""
    openai_base_url: str = "https://maas-llm-aiplatform-hcm.api.vngcloud.vn/v1"
    openai_model: str = "qwen/qwen3.7-plus"
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
