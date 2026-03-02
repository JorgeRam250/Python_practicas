"""Puertos de aplicacion para repositorios, eventos y transacciones."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Protocol
from uuid import UUID

from src.domain.customers.entities import Customer
from src.domain.orders.entities import Order, OrderStatus
from src.domain.products.entities import Product


class CustomerRepositoryPort(Protocol):
    """Contrato para almacenamiento de clientes."""

    def add(self, customer: Customer) -> None:
        """Guarda un cliente."""

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        """Busca cliente por identificador."""

    def get_by_email(self, email: str) -> Customer | None:
        """Busca cliente por email normalizado."""

    def list(self) -> list[Customer]:
        """Lista clientes ordenados para consulta operacional."""


class ProductRepositoryPort(Protocol):
    """Contrato para almacenamiento de productos."""

    def add(self, product: Product) -> None:
        """Guarda un producto."""

    def get_by_id(self, product_id: UUID) -> Product | None:
        """Busca producto por identificador."""

    def get_by_sku(self, sku: str) -> Product | None:
        """Busca producto por sku."""

    def list(self) -> list[Product]:
        """Lista productos ordenados para consulta operacional."""


class OrderRepositoryPort(Protocol):
    """Contrato para almacenamiento de ordenes."""

    def add(self, order: Order) -> None:
        """Guarda una orden nueva."""

    def update(self, order: Order) -> None:
        """Actualiza una orden existente."""

    def get_by_id(self, order_id: UUID) -> Order | None:
        """Busca orden por identificador."""

    def list(self, status: OrderStatus | None = None) -> list[Order]:
        """Lista ordenes con filtro opcional de estado."""


@dataclass(frozen=True, slots=True)
class InvoiceRecord:
    """Registro de factura emitida fuera del core transaccional."""

    order_id: UUID
    external_invoice_id: str
    total_amount: Decimal


class InvoiceRepositoryPort(Protocol):
    """Contrato para registrar facturas emitidas por sistemas externos."""

    def add(self, record: InvoiceRecord) -> None:
        """Guarda un registro de factura."""

    def get_by_order_id(self, order_id: UUID) -> InvoiceRecord | None:
        """Busca registro de factura por orden."""


class EventPublisherPort(Protocol):
    """Contrato para publicar eventos de aplicacion."""

    def publish(self, event_name: str, payload: Mapping[str, Any]) -> None:
        """Publica un evento de dominio/aplicacion."""


class UnitOfWorkPort(Protocol):
    """Contrato minimo de transaccion para casos de uso."""

    def commit(self) -> None:
        """Confirma cambios de una unidad de trabajo."""

    def rollback(self) -> None:
        """Revierte cambios de una unidad de trabajo."""
