"""Settings de infraestructura cargados desde variables de entorno."""

from __future__ import annotations

import os

from pydantic import BaseModel, ConfigDict, Field


class InfrastructureSettings(BaseModel):
    """Configuracion tipada para adaptadores de infraestructura."""

    model_config = ConfigDict(frozen=True)

    service_name: str = Field(default="distrito-chilaquil")
    api_version: str = Field(default="0.1.0")
    log_level: str = Field(default="INFO")
    request_id_header: str = Field(default="X-Request-ID")
    healthcheck_timeout_seconds: float = Field(default=1.0)
    cors_allowed_origins: tuple[str, ...] = Field(
        default=(
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://127.0.0.1:5501",
            "http://localhost:5501",
        )
    )
    cors_allowed_methods: tuple[str, ...] = Field(default=("GET", "POST", "PATCH", "OPTIONS"))
    cors_allowed_headers: tuple[str, ...] = Field(default=("*",))
    cors_allow_credentials: bool = Field(default=False)

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/distrito_chilaquil"
    )
    database_echo: bool = Field(default=False)

    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    kafka_client_id: str = Field(default="distrito-chilaquil-api")
    kafka_topic_orders: str = Field(default="orders.v1")
    kafka_enabled: bool = Field(default=True)

    @classmethod
    def from_env(cls) -> InfrastructureSettings:
        """Construye settings a partir del entorno."""
        # Se usa pydantic para convertir tipos de forma segura.
        raw_data = {
            "service_name": os.getenv("SERVICE_NAME", "distrito-chilaquil"),
            "api_version": os.getenv("API_VERSION", "0.1.0"),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "request_id_header": os.getenv("REQUEST_ID_HEADER", "X-Request-ID"),
            "healthcheck_timeout_seconds": os.getenv("HEALTHCHECK_TIMEOUT_SECONDS", "1.0"),
            # Comentario para junior: CORS habilita que la UI estatica local llame la API.
            "cors_allowed_origins": _csv_env(
                os.getenv(
                    "CORS_ALLOWED_ORIGINS",
                    ",".join(
                        [
                            "http://127.0.0.1:5500",
                            "http://localhost:5500",
                            "http://127.0.0.1:5501",
                            "http://localhost:5501",
                        ]
                    ),
                )
            ),
            "cors_allowed_methods": _csv_env(
                os.getenv("CORS_ALLOWED_METHODS", "GET,POST,PATCH,OPTIONS")
            ),
            "cors_allowed_headers": _csv_env(os.getenv("CORS_ALLOWED_HEADERS", "*")),
            "cors_allow_credentials": os.getenv("CORS_ALLOW_CREDENTIALS", "false"),
            "database_url": os.getenv(
                "DATABASE_URL",
                "postgresql+asyncpg://postgres:postgres@localhost:5432/distrito_chilaquil",
            ),
            "database_echo": os.getenv("DATABASE_ECHO", "false"),
            "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            "kafka_client_id": os.getenv("KAFKA_CLIENT_ID", "distrito-chilaquil-api"),
            "kafka_topic_orders": os.getenv("KAFKA_TOPIC_ORDERS", "orders.v1"),
            "kafka_enabled": os.getenv("KAFKA_ENABLED", "true"),
        }
        return cls.model_validate(raw_data)


def _csv_env(value: str) -> tuple[str, ...]:
    """Convierte string separado por comas en tupla limpia."""
    return tuple(item.strip() for item in value.split(",") if item.strip())
