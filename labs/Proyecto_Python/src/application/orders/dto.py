"""DTOs internos de aplicacion para ordenes."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.orders.entities import OrderStatus


@dataclass(frozen=True, slots=True)
class CreateOrderItemInput:
    """Linea solicitada para crear una orden."""

    product_id: UUID
    quantity: int


@dataclass(frozen=True, slots=True)
class CreateOrderCommand:
    """Comando para crear una orden."""

    customer_id: UUID
    branch_id: str
    items: tuple[CreateOrderItemInput, ...]
    shipping_cost: Decimal = Decimal("0")
    tax_rate: Decimal = Decimal("0.16")


@dataclass(frozen=True, slots=True)
class GetOrderQuery:
    """Consulta para obtener una orden por id."""

    order_id: UUID


@dataclass(frozen=True, slots=True)
class ListOrdersQuery:
    """Consulta para listar ordenes."""

    status: OrderStatus | None = None


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusCommand:
    """Comando para cambiar el estado de una orden."""

    order_id: UUID
    target_status: OrderStatus
    cancellation_reason: str | None = None


@dataclass(frozen=True, slots=True)
class OrderItemDTO:
    """Representacion de una linea de orden."""

    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal


@dataclass(frozen=True, slots=True)
class OrderDTO:
    """Representacion de salida para ordenes."""

    order_id: UUID
    customer_id: UUID
    customer_email: str
    branch_id: str
    status: OrderStatus
    cancellation_reason: str | None
    items: tuple[OrderItemDTO, ...]
    shipping_cost: Decimal
    tax_rate: Decimal
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal
