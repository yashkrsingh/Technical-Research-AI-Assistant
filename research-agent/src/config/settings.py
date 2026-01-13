from __future__ import annotations
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_env_file(start: Path, max_up: int = 6) -> Optional[Path]:
    cur = start.resolve()
    for _ in range(max_up):
        candidate = cur / ".env"
        if candidate.exists():
            return candidate
        cur = cur.parent
    return None


_ENV_FILE = _find_env_file(Path(__file__).resolve())


class SupabaseDBConfig(BaseModel):
    connection_string: str
    db_schema: str


class ApiServerConfig(BaseModel):
    host: str
    port: int
    log_level: str
    auth_key: str


class LLMConfig(BaseModel):
    openai_api_key: Optional[str]


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE else None,
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    local: bool = Field(default=False, alias="LOCAL")
    app_mode: Literal["api"] = Field(default="api", alias="APP_MODE")

    # API
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    log_level: str = Field(default="INFO", alias="LOGURU_LEVEL")

    # LLM
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")

    # Supabase
    supabase_connection_string: str = Field(default="", alias="SUPABASE_CONNECTION_STRING")
    supabase_schema: str = Field(default="public", alias="SUPABASE_SCHEMA")

    # API Authentication
    auth_key: Optional[str] = Field(default=None, alias="AUTH_KEY")

    @property
    def api(self) -> ApiServerConfig:
        return ApiServerConfig(
            host=self.app_host,
            port=self.app_port,
            log_level=self.log_level,
            auth_key=self.auth_key,
        )

    @property
    def llm(self) -> LLMConfig:
        return LLMConfig(
            openai_api_key=self.openai_api_key,
        )

    @property
    def supabase(self) -> SupabaseDBConfig:
        return SupabaseDBConfig(
            connection_string=self.supabase_connection_string,
            db_schema=self.supabase_schema,
        )


configuration = Configuration()
