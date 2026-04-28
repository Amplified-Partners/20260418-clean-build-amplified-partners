"""
OpenClaw Agent Service Configuration
=====================================
Single source of truth for all service connections.
Everything routes through LiteLLM — no direct provider keys here.
Beast Docker network IPs used for service-to-service comms.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- FastAPI ---
    APP_NAME: str = "openclaw-agents"
    APP_VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8100
    DEBUG: bool = False

    # --- LiteLLM (model router — all LLM calls go through here) ---
    LITELLM_BASE_URL: str = "http://litellm:4000"
    LITELLM_API_KEY: SecretStr = SecretStr("sk-c9dbd5b4276fea7562d8ff1a72b001dfb833b8048f13ae24bd3474e4e8518d5c")
    # Default model for agents unless overridden per-agent
    DEFAULT_MODEL: str = "gpt-4.1-mini"

    # --- PostgreSQL (checkpointing + long-term memory) ---
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "amplified_main"
    POSTGRES_USER: str = "amplified"
    POSTGRES_PASSWORD: SecretStr = SecretStr("sJAFpRhxMNtT/LaR7HlxdvpZwlQJymIth15osijkLxY=")
    POSTGRES_MIN_CONNECTIONS: int = 2
    POSTGRES_MAX_CONNECTIONS: int = 10

    @property
    def postgres_dsn(self) -> str:
        from urllib.parse import quote
        encoded_pw = quote(self.POSTGRES_PASSWORD.get_secret_value(), safe="")
        return (
            f"postgresql://{self.POSTGRES_USER}:{encoded_pw}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --- Redis (caching) ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 1  # DB 0 is LiteLLM cache

    # --- Langfuse (observability) ---
    LANGFUSE_HOST: str = "http://langfuse:3000"
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: SecretStr = SecretStr("")

    # --- SearXNG (search) ---
    SEARXNG_BASE_URL: str = "http://searxng:8080"

    # --- Auth ---
    API_KEY: SecretStr = SecretStr("openclaw-dev-key-change-me")


settings = Settings()
