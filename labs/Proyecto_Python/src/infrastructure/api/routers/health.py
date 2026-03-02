"""Router de salud del servicio."""

from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Literal, cast

import asyncpg  # type: ignore[import-untyped]
from fastapi import APIRouter, Request

from src.infrastructure.api.dependencies import ApiContainer
from src.infrastructure.api.schemas.health import (
    HealthCheckDetail,
    HealthReadinessResponse,
    HealthResponse,
)
from src.infrastructure.settings import InfrastructureSettings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def get_health(request: Request) -> HealthResponse:
    """Endpoint liveness rapido para monitoreo base."""
    settings = _resolve_settings(request)
    return HealthResponse(status="ok", service=settings.service_name)


@router.get("/ready", response_model=HealthReadinessResponse)
async def get_readiness(request: Request) -> HealthReadinessResponse:
    """Endpoint readiness con comprobaciones de DB y conectividad Kafka."""
    settings = _resolve_settings(request)
    container = cast(ApiContainer | None, getattr(request.app.state, "container", None))
    if container is None:
        checks = {
            "database": HealthCheckDetail(
                status="unknown",
                detail="No hay contenedor de infraestructura en app.state.container.",
            ),
            "kafka": HealthCheckDetail(
                status="unknown",
                detail="No hay contenedor de infraestructura en app.state.container.",
            ),
        }
        return HealthReadinessResponse(
            status="degraded",
            service=settings.service_name,
            checks=checks,
        )

    database_check = await _check_database(
        database_url=settings.database_url,
        timeout_seconds=settings.healthcheck_timeout_seconds,
    )
    kafka_check = await _check_kafka(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        kafka_enabled=settings.kafka_enabled,
        timeout_seconds=settings.healthcheck_timeout_seconds,
    )
    checks = {
        "database": database_check,
        "kafka": kafka_check,
    }
    return HealthReadinessResponse(
        status=_resolve_overall_status(checks=checks),
        service=settings.service_name,
        checks=checks,
    )


def _resolve_settings(request: Request) -> InfrastructureSettings:
    """Obtiene settings pre-cargados en la app o usa defaults de entorno."""
    settings = getattr(request.app.state, "settings", None)
    if isinstance(settings, InfrastructureSettings):
        return settings
    return InfrastructureSettings.from_env()


def _resolve_overall_status(
    checks: dict[str, HealthCheckDetail],
) -> Literal["ok", "degraded", "error"]:
    """Calcula estado global usando el peor estado detectado."""
    statuses = [check.status for check in checks.values()]
    if any(status == "error" for status in statuses):
        return "error"
    if all(status in {"ok", "disabled"} for status in statuses):
        return "ok"
    return "degraded"


async def _check_database(database_url: str, timeout_seconds: float) -> HealthCheckDetail:
    """Verifica conectividad DB con una consulta minima por conexion dedicada."""
    asyncpg_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    connection: asyncpg.Connection | None = None
    try:
        async with asyncio.timeout(timeout_seconds):
            connection = await asyncpg.connect(asyncpg_url)
            await connection.fetchval("SELECT 1")
        return HealthCheckDetail(status="ok", detail="Conexion SQL operativa.")
    except Exception as exc:  # noqa: BLE001 - endpoint de salud requiere capturar fallos.
        return HealthCheckDetail(status="error", detail=f"Fallo al consultar DB: {exc!s}")
    finally:
        if connection is not None:
            with suppress(Exception):
                await connection.close()


async def _check_kafka(
    bootstrap_servers: str,
    kafka_enabled: bool,
    timeout_seconds: float,
) -> HealthCheckDetail:
    """Verifica conectividad TCP basica contra el primer bootstrap server."""
    if not kafka_enabled:
        return HealthCheckDetail(status="disabled", detail="Kafka deshabilitado por configuracion.")

    first_server = bootstrap_servers.split(",")[0].strip()
    host, separator, raw_port = first_server.partition(":")
    if separator == "" or not raw_port.isdigit():
        return HealthCheckDetail(
            status="error",
            detail="KAFKA_BOOTSTRAP_SERVERS debe tener formato host:port.",
        )

    writer: asyncio.StreamWriter | None = None
    try:
        async with asyncio.timeout(timeout_seconds):
            _, writer = await asyncio.open_connection(host, int(raw_port))
        return HealthCheckDetail(status="ok", detail=f"Broker reachable en {first_server}.")
    except Exception as exc:  # noqa: BLE001 - endpoint de salud requiere capturar fallos.
        return HealthCheckDetail(status="error", detail=f"No se pudo conectar a Kafka: {exc!s}")
    finally:
        if writer is not None:
            writer.close()
            with suppress(Exception):
                await writer.wait_closed()
