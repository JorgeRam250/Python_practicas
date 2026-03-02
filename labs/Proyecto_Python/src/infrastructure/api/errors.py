"""Mapeo consistente de errores de aplicacion a HTTP."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.application.errors import (
    ApplicationConflictError,
    ApplicationDependencyError,
    ApplicationNotFoundError,
    ApplicationValidationError,
)
from src.infrastructure.api.schemas.common import ErrorDetail, ErrorResponse


def _build_error_response(http_status: int, code: str, message: str) -> JSONResponse:
    """Construye payload de error uniforme."""
    payload = ErrorResponse(error=ErrorDetail(code=code, message=message))
    return JSONResponse(status_code=http_status, content=payload.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    """Registra manejo global de errores para la API."""

    @app.exception_handler(ApplicationValidationError)
    def handle_application_validation_error(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: ApplicationValidationError,
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_422_UNPROCESSABLE_CONTENT,
            code="application_validation_error",
            message=str(exc),
        )

    @app.exception_handler(ApplicationNotFoundError)
    def handle_application_not_found_error(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: ApplicationNotFoundError,
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_404_NOT_FOUND,
            code="application_not_found_error",
            message=str(exc),
        )

    @app.exception_handler(ApplicationConflictError)
    def handle_application_conflict_error(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: ApplicationConflictError,
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_409_CONFLICT,
            code="application_conflict_error",
            message=str(exc),
        )

    @app.exception_handler(ApplicationDependencyError)
    def handle_application_dependency_error(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: ApplicationDependencyError,
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="application_dependency_error",
            message=str(exc),
        )

    @app.exception_handler(RequestValidationError)
    def handle_request_validation_error(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_422_UNPROCESSABLE_CONTENT,
            code="request_validation_error",
            message=str(exc),
        )

    @app.exception_handler(Exception)
    def handle_unhandled_exception(
        request: Request,  # noqa: ARG001 - firmado requerido por FastAPI.
        exc: Exception,  # noqa: BLE001 - handler global controlado.
    ) -> JSONResponse:
        return _build_error_response(
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="internal_server_error",
            message="Error interno no controlado.",
        )
