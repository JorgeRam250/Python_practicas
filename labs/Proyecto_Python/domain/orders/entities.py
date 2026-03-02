"""Entidades y agregado principal de ordenes."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import UUID

from src.domain.customers.entities import Customer
from src.domain.products.entities import Product

from .exceptions import DomainValidationError, InvalidOrderStateTransitionError
from .value_objects import (
    normalize_money,
    validate_non_empty_text,
    validate_non_negative_money,
    validate_positive_quantity,
    validate_tax_rate,
)


class OrderStatus(Enum):
    """Estados validos del ciclo de vida de una orden."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


_ALLOWED_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.IN_PROGRESS, OrderStatus.CANCELLED},
    OrderStatus.IN_PROGRESS: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.COMPLETED},
    OrderStatus.COMPLETED: set(),
    OrderStatus.CANCELLED: set(),
}


@dataclass(frozen=True, slots=True)
class OrderItem:
    """Snapshot del producto comprado dentro de una orden."""

    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "product_name", validate_non_empty_text(self.product_name, "product_name")
        )
        object.__setattr__(self, "quantity", validate_positive_quantity(self.quantity))
        normalized_price = validate_non_negative_money(self.unit_price, "unit_price")
        object.__setattr__(self, "unit_price", normalized_price)

    @property
    def subtotal(self) -> Decimal:
        """Subtotal del item, ya normalizado a 2 decimales."""
        return normalize_money(self.unit_price * Decimal(self.quantity))

    @classmethod
    def from_product(cls, product: Product, quantity: int) -> OrderItem:
        """Crea un item tomando snapshot del producto para mantener trazabilidad."""
        return cls(
            product_id=product.product_id,
            product_name=product.name,
            unit_price=product.unit_price,
            quantity=quantity,
        )


@dataclass(slots=True)
class Order:
    """Agregado raiz de ordenes."""

    order_id: UUID
    customer: Customer
    branch_id: str
    items: list[OrderItem] = field(default_factory=list)
    shipping_cost: Decimal = Decimal("0")
    tax_rate: Decimal = Decimal("0.16")
    status: OrderStatus = OrderStatus.PENDING
    cancellation_reason: str | None = None

    def __post_init__(self) -> None:
        self.branch_id = validate_non_empty_text(self.branch_id, "branch_id")
        if not self.items:
            raise DomainValidationError("Una orden debe contener al menos un item.")

        self.shipping_cost = validate_non_negative_money(self.shipping_cost, "shipping_cost")
        self.tax_rate = validate_tax_rate(self.tax_rate)

        if self.status is OrderStatus.CANCELLED and not self.cancellation_reason:
            raise DomainValidationError(
                "Una orden en estado CANCELLED requiere cancellation_reason."
            )

        if self.status is not OrderStatus.CANCELLED and self.cancellation_reason is not None:
            raise DomainValidationError(
                "cancellation_reason solo puede existir cuando la orden esta cancelada."
            )

    @property
    def subtotal(self) -> Decimal:
        """Subtotal de la orden sumando subtotales de items."""
        amount = sum((item.subtotal for item in self.items), start=Decimal("0"))
        return normalize_money(amount)

    @property
    def tax_total(self) -> Decimal:
        """Impuesto calculado sobre subtotal en escala decimal."""
        return normalize_money(self.subtotal * self.tax_rate)

    @property
    def total(self) -> Decimal:
        """Total final de la orden."""
        return normalize_money(self.subtotal + self.tax_total + self.shipping_cost)

    def add_item(self, item: OrderItem) -> None:
        """Agrega un item solo mientras la orden no avance de estado."""
        if self.status is not OrderStatus.PENDING:
            raise DomainValidationError("Solo se pueden agregar items en estado PENDING.")
        self.items.append(item)

    def update_shipping_cost(self, shipping_cost: Decimal) -> None:
        """Actualiza costo de envio mientras la orden este pendiente."""
        if self.status is not OrderStatus.PENDING:
            raise DomainValidationError("Solo se puede cambiar shipping_cost en estado PENDING.")
        self.shipping_cost = validate_non_negative_money(shipping_cost, "shipping_cost")

    def start_processing(self) -> None:
        """Mueve la orden a preparacion."""
        self._transition_to(OrderStatus.IN_PROGRESS)

    def mark_shipped(self) -> None:
        """Marca la orden como enviada."""
        self._transition_to(OrderStatus.SHIPPED)

    def complete(self) -> None:
        """Marca la orden como completada."""
        self._transition_to(OrderStatus.COMPLETED)

    def cancel(self, reason: str) -> None:
        """Cancela la orden guardando la razon de negocio."""
        self._transition_to(OrderStatus.CANCELLED)
        self.cancellation_reason = validate_non_empty_text(reason, "cancellation_reason")

    def cancel_due_payment_failure(self) -> None:
        """Alias de negocio para el caso 'cancelar si el pago no paso'."""
        self.cancel("payment_failed")

    def _transition_to(self, target_status: OrderStatus) -> None:
        """Aplica la matriz de transiciones permitidas del agregado."""
        allowed_targets = _ALLOWED_TRANSITIONS[self.status]
        if target_status not in allowed_targets:
            raise InvalidOrderStateTransitionError(self.status.value, target_status.value)
        self.status = target_status
