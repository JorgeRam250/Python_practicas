"""Schemas comunes para respuestas HTTP de la API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ApiBaseModel(BaseModel):
    """Base de schemas API con serializacion consistente."""

    # Comentario para junior: dejamos configuracion centralizada para futuros ajustes de API.
    model_config = ConfigDict()


class ErrorDetail(ApiBaseModel):
    """Detalle estandar de error."""

    code: str
    message: str


class ErrorResponse(ApiBaseModel):
    """Payload estandar de errores API."""

    error: ErrorDetail
