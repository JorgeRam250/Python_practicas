"""Entidades del subdominio de productos."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.domain.orders.value_objects import (
    validate_non_empty_text,
    validate_non_negative_money,
)


@dataclass(frozen=True, slots=True)
class Product:
    """Entidad producto del catalogo operacional."""

    product_id: UUID
    sku: str
    name: str
    unit_price: Decimal
    is_active: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "sku", validate_non_empty_text(self.sku, "sku"))
        object.__setattr__(self, "name", validate_non_empty_text(self.name, "name"))
        normalized_price = validate_non_negative_money(self.unit_price, "unit_price")
        object.__setattr__(self, "unit_price", normalized_price)
