"""Observabilidad minima para trazabilidad de requests HTTP."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response


def configure_logging(log_level: str) -> None:
    """Configura logging base del servicio con formato uniforme."""
    resolved_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=resolved_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def register_request_logging_middleware(app: FastAPI, request_id_header: str) -> None:
    """Registra middleware para loggear cada request y propagar request id."""
    logger = logging.getLogger("distrito_chilaquil.api")

    @app.middleware("http")
    async def request_logging_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get(request_id_header) or str(uuid4())
        start_time = perf_counter()
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - start_time) * 1000, 2)
            # Comentario para junior: se deja evidencia de excepcion con contexto tecnico.
            logger.exception(
                "request_failed method=%s path=%s status=%s duration_ms=%s request_id=%s",
                method,
                path,
                500,
                duration_ms,
                request_id,
            )
            raise

        duration_ms = round((perf_counter() - start_time) * 1000, 2)
        response.headers[request_id_header] = request_id
        logger.info(
            "request_completed method=%s path=%s status=%s duration_ms=%s request_id=%s",
            method,
            path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response
