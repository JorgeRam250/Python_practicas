"""Publicador base de eventos con aiokafka."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from aiokafka import AIOKafkaProducer  # type: ignore[import-untyped]

from src.application.ports import EventPublisherPort
from src.infrastructure.common.async_runner import run_sync
from src.infrastructure.settings import InfrastructureSettings


class AIOKafkaEventPublisher(EventPublisherPort):
    """Implementacion base de publicacion en Kafka."""

    def __init__(self, settings: InfrastructureSettings) -> None:
        self._settings = settings

    def publish(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Publica evento serializado en JSON.

        Si Kafka esta deshabilitado por configuracion, no-op controlado.
        """
        if not self._settings.kafka_enabled:
            return
        run_sync(self._publish_once(event_name, payload))

    async def _publish_once(self, event_name: str, payload: Mapping[str, Any]) -> None:
        producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.kafka_bootstrap_servers,
            client_id=self._settings.kafka_client_id,
        )
        await producer.start()
        try:
            message_payload = {
                "event_name": event_name,
                "payload": dict(payload),
            }
            encoded_payload = json.dumps(message_payload, ensure_ascii=True).encode("utf-8")
            await producer.send_and_wait(self._settings.kafka_topic_orders, encoded_payload)
        finally:
            await producer.stop()
