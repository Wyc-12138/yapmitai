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
    database_url: str = "postgresql+asyncpg://yapmitai:yapmitai@localhost:5432/yapmitai"
    redis_url: str = "redis://localhost:6379/0"
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    enable_mock_fallback: bool = True
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [value.strip() for value in self.cors_origins.split(",") if value.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
