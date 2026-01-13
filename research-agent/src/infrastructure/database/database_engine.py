import uuid
from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from infrastructure.database.config_service import ConfigService


def _normalize_async_url(url: str) -> str:
    if not url:
        return url
    # Upgrade to async driver prefix if needed
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://") :]
    if url.startswith("postgresql://") and "+" not in url.split("://", 1)[0]:
        return "postgresql+asyncpg://" + url[len("postgresql://") :]
    return url


class DatabaseEngine:
    _engine: Optional[AsyncEngine] = None
    _config_service: Optional[ConfigService] = None

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        """Get or create the shared database engine"""
        if cls._engine is None:
            cls._engine = cls._create_engine()
            logger.info("Database engine created and initialized")
        return cls._engine

    @classmethod
    def _create_engine(cls) -> AsyncEngine:
        """Create the database engine with optimized settings"""
        if cls._config_service is None:
            cls._config_service = ConfigService()

        supabase_config = cls._config_service.supabaseConfig
        raw_url = (supabase_config.connection_string or "").strip()
        conn_url = _normalize_async_url(raw_url)

        if not conn_url:
            raise ValueError(
                "SUPABASE connection string is empty. Set SUPABASE_CONNECTION_STRING in your environment or settings."
            )

        try:
            masked = conn_url
            if "@" in masked:
                masked = masked.split("@", 1)[-1]
            logger.info(f"Creating async engine for host/db (sanitized): {masked}")
        except Exception:
            logger.info("Creating async engine...")

        return create_async_engine(
            conn_url,
            echo=False,
            future=True,

            pool_size=5,
            max_overflow=15,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,

            connect_args={
                "prepared_statement_name_func": lambda: f"__asyncpg_{uuid.uuid4()}__",
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
                "command_timeout": 60,
                "server_settings": {"application_name": "codeskin"},
            }
        )

    @classmethod
    async def close_engine(cls):
        """Close the database engine and all connections"""
        if cls._engine:
            logger.info("Closing database engine and connection pool")
            await cls._engine.dispose()
            cls._engine = None
            cls._config_service = None
            logger.info("Database engine closed")
