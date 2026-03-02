"""Adaptadores de eventos para infraestructura."""

from .kafka_publisher import AIOKafkaEventPublisher

__all__ = ["AIOKafkaEventPublisher"]
