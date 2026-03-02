"""DTOs internos de aplicacion para productos."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateProductCommand:
    """Comando para crear un producto."""

    sku: str
    name: str
    unit_price: Decimal
    is_active: bool = True


@dataclass(frozen=True, slots=True)
class ProductDTO:
    """Representacion de salida para productos."""

    product_id: UUID
    sku: str
    name: str
    unit_price: Decimal
    is_active: bool
