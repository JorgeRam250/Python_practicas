"""Entrada principal de FastAPI para Distrito Chilaquil."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.api.dependencies import ApiContainer
from src.infrastructure.api.errors import register_exception_handlers
from src.infrastructure.api.observability import (
    configure_logging,
    register_request_logging_middleware,
)
from src.infrastructure.api.routers import (
    customers_router,
    health_router,
    orders_router,
    products_router,
)
from src.infrastructure.db.session import build_async_engine, build_session_factory
from src.infrastructure.events.kafka_publisher import AIOKafkaEventPublisher
from src.infrastructure.settings import InfrastructureSettings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Inicializa y libera recursos de infraestructura."""
    existing_container = getattr(app.state, "container", None)
    if existing_container is not None:
        # Comentario para junior: se respeta el contenedor inyectado por tests.
        yield
        return

    settings = cast(InfrastructureSettings, app.state.settings)
    engine = build_async_engine(settings)
    session_factory = build_session_factory(engine)
    event_publisher = AIOKafkaEventPublisher(settings=settings)

    app.state.container = ApiContainer(
        settings=settings,
        engine=engine,
        session_factory=session_factory,
        event_publisher=event_publisher,
    )
    yield
    await engine.dispose()


def create_app(settings: InfrastructureSettings | None = None) -> FastAPI:
    """Construye la aplicacion FastAPI con routers y handlers."""
    resolved_settings = settings or InfrastructureSettings.from_env()
    configure_logging(resolved_settings.log_level)

    app = FastAPI(
        title="Distrito Chilaquil API",
        version=resolved_settings.api_version,
        lifespan=lifespan,
    )
    # Comentario para junior: sin CORS la UI estatica del puerto 5500/5501 no puede consultar la API.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(resolved_settings.cors_allowed_origins),
        allow_credentials=resolved_settings.cors_allow_credentials,
        allow_methods=list(resolved_settings.cors_allowed_methods),
        allow_headers=list(resolved_settings.cors_allowed_headers),
    )
    app.state.settings = resolved_settings
    register_exception_handlers(app)
    register_request_logging_middleware(app, request_id_header=resolved_settings.request_id_header)

    app.include_router(health_router)
    app.include_router(customers_router)
    app.include_router(products_router)
    app.include_router(orders_router)

    return app


app = create_app()
