from typing import Annotated
from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class BaseConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", frozen=True)


class Settings(BaseConfigSettings):
    # Application
    app_version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"
    service_name: str = "rag-api"

    # PostgreSQL
    postgres_database_url: str = (
        "postgresql+psycopg2://rag_user:rag_password@localhost:5432/rag_db"
    )
    postgres_echo_sql: bool = False
    postgres_pool_size: int = 20
    postgres_max_overflow: int = 0

    # OpenSearch
    opensearch_host: str = "http://localhost:9200"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_models: Annotated[list[str], NoDecode] = ["llama3.2:1b"]
    ollama_default_model: str = "llama3.2:1b"
    ollama_timeout: int = 300

    @field_validator("ollama_models", mode="before")
    @classmethod
    def parse_ollama_models(cls, v: str | list[str]) -> list[str]:
        """Split a comma-separated string from .env into a list of model names."""
        if isinstance(v, str):
            return [model.strip() for model in v.split(",") if model.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
