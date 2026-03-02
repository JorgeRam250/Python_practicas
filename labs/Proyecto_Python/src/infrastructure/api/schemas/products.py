"""Schemas API para productos."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import Field

from src.application.products.dto import ProductDTO

from .common import ApiBaseModel


class CreateProductRequest(ApiBaseModel):
    """Payload de alta de producto."""

    sku: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    unit_price: Decimal = Field(ge=0)
    is_active: bool = True


class ProductResponse(ApiBaseModel):
    """Respuesta HTTP de producto."""

    product_id: UUID
    sku: str
    name: str
    unit_price: Decimal
    is_active: bool

    @classmethod
    def from_dto(cls, dto: ProductDTO) -> ProductResponse:
        """Mapea DTO de aplicacion a schema de respuesta."""
        return cls(
            product_id=dto.product_id,
            sku=dto.sku,
            name=dto.name,
            unit_price=dto.unit_price,
            is_active=dto.is_active,
        )
