"""Construccion de engine y factory de sesiones async."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.settings import InfrastructureSettings


def build_async_engine(settings: InfrastructureSettings) -> AsyncEngine:
    """Construye engine async para PostgreSQL."""
    return create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
    )


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Construye la fabrica de sesiones async."""
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
