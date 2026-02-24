from __future__ import annotations

from src.order_entity import Order
from src.order_models import OrderIn, OrderOut


def to_entity(order_in: OrderIn) -> Order:
    """Convierte un modelo de entrada validado a la entidad de dominio."""

    return Order(
        id=order_in.id,
        customer_name=order_in.customer_name,
        unit_price=order_in.unit_price,
        quantity=order_in.quantity,
        tax_rate=order_in.tax_rate,
    )


def to_output(order: Order) -> OrderOut:
    """Convierte una entidad de dominio a un modelo de salida serializable."""

    return OrderOut(
        id=order.id,
        customer_name=order.customer_name,
        unit_price=order.unit_price,
        quantity=order.quantity,
        tax_rate=order.tax_rate,
        subtotal=order.subtotal,
        tax_amount=order.tax_amount,
        total=order.total,
    )
