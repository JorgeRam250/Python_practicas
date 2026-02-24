from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True)
class Order:
    """Entidad de dominio que representa una orden de compra."""

    sort_index: float = field(init=False, repr=False)
    id: int = field(compare=False)
    customer_name: str = field(compare=False)
    unit_price: float = field(compare=False)
    quantity: int = field(compare=False)
    tax_rate: float = field(default=0.18, compare=False)

    def __post_init__(self) -> None:
        if self.unit_price <= 0:
            raise ValueError("unit_price debe ser mayor que 0")
        if self.quantity <= 0:
            raise ValueError("quantity debe ser mayor que 0")
        if not (0 <= self.tax_rate <= 1):
            raise ValueError("tax_rate debe estar entre 0 y 1")
        if not self.customer_name.strip():
            raise ValueError("customer_name no puede estar vacio")

        self.sort_index = self.total

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)

    @property
    def tax_amount(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax_amount, 2)

    def __str__(self) -> str:
        return (
            f"Order(id={self.id}, customer='{self.customer_name}', "
            f"subtotal={self.subtotal}, tax={self.tax_amount}, total={self.total})"
        )
