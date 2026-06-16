from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "YAPMITAI Backend"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    api_key: str = "yap_demo_key_2026"
    agent_gateway_url: str = "https://gateway.yapmitai.com/api/v1"
    agent_gateway_token: str = ""
    agent_timeout_seconds: int = 30
    database_url: str = (
        "mysql+aiomysql://root:change_me@localhost:3306/yapmitai?charset=utf8mb4"
    )
    redis_url: str = "redis://localhost:6379/0"
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_persist_dir: str = "storage/chroma"
    enable_mock_fallback: bool = True
    cors_origins: str = "http://localhost:5173"
    external_ai_base_url: str = "https://api.openai.com/v1"
    external_ai_api_key: str = ""
    embedding_models: str = "text-embedding-3-small,text-embedding-3-large"
    answer_models: str = "gpt-4o-mini,gpt-4.1-mini"
    knowledge_storage_dir: str = "storage/knowledge"
    growth_reports_dir: str = "storage/growth-reports"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]

    @property
    def embedding_model_list(self) -> list[str]:
        return [value.strip() for value in self.embedding_models.split(",") if value.strip()]

    @property
    def answer_model_list(self) -> list[str]:
        return [value.strip() for value in self.answer_models.split(",") if value.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
