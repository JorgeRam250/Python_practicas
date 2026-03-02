"""Schemas de health check."""

from __future__ import annotations

from typing import Literal

from .common import ApiBaseModel


class HealthResponse(ApiBaseModel):
    """Respuesta de verificacion de salud."""

    status: str
    service: str


class HealthCheckDetail(ApiBaseModel):
    """Detalle de una comprobacion de readiness."""

    status: Literal["ok", "disabled", "error", "unknown"]
    detail: str


class HealthReadinessResponse(ApiBaseModel):
    """Respuesta util para readiness operativa."""

    status: Literal["ok", "degraded", "error"]
    service: str
    checks: dict[str, HealthCheckDetail]
