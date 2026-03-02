"""Schemas API para ordenes."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import Field

from src.application.orders.dto import OrderDTO, OrderItemDTO
from src.domain.orders.entities import OrderStatus

from .common import ApiBaseModel


class OrderStatusEnum(str, Enum):
    """Estados expuestos por contrato HTTP."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    def to_domain(self) -> OrderStatus:
        """Convierte estado de API a estado de dominio."""
        return OrderStatus(self.value)


class CreateOrderItemRequest(ApiBaseModel):
    """Linea de producto para crear orden."""

    product_id: UUID
    quantity: int = Field(gt=0)


class CreateOrderRequest(ApiBaseModel):
    """Payload de alta de orden."""

    customer_id: UUID
    branch_id: str = Field(min_length=1, max_length=100)
    items: list[CreateOrderItemRequest] = Field(min_length=1)
    shipping_cost: Decimal = Field(default=Decimal("0"), ge=0)
    tax_rate: Decimal = Field(default=Decimal("0.16"), ge=0, le=1)


class UpdateOrderStatusRequest(ApiBaseModel):
    """Payload para cambio de estado."""

    target_status: OrderStatusEnum
    cancellation_reason: str | None = Field(default=None, max_length=255)


class OrderItemResponse(ApiBaseModel):
    """Item de orden en respuestas API."""

    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal

    @classmethod
    def from_dto(cls, dto: OrderItemDTO) -> OrderItemResponse:
        """Mapea DTO de item a response."""
        return cls(
            product_id=dto.product_id,
            product_name=dto.product_name,
            unit_price=dto.unit_price,
            quantity=dto.quantity,
            subtotal=dto.subtotal,
        )


class OrderResponse(ApiBaseModel):
    """Respuesta HTTP de orden."""

    order_id: UUID
    customer_id: UUID
    customer_email: str
    branch_id: str
    status: OrderStatusEnum
    cancellation_reason: str | None
    items: tuple[OrderItemResponse, ...]
    shipping_cost: Decimal
    tax_rate: Decimal
    subtotal: Decimal
    tax_total: Decimal
    total: Decimal

    @classmethod
    def from_dto(cls, dto: OrderDTO) -> OrderResponse:
        """Mapea DTO de orden a schema de respuesta."""
        return cls(
            order_id=dto.order_id,
            customer_id=dto.customer_id,
            customer_email=dto.customer_email,
            branch_id=dto.branch_id,
            status=OrderStatusEnum(dto.status.value),
            cancellation_reason=dto.cancellation_reason,
            items=tuple(OrderItemResponse.from_dto(item) for item in dto.items),
            shipping_cost=dto.shipping_cost,
            tax_rate=dto.tax_rate,
            subtotal=dto.subtotal,
            tax_total=dto.tax_total,
            total=dto.total,
        )
