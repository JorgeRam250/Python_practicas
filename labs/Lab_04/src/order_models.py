from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OrderIn(BaseModel):
    """Datos de entrada validados."""

    model_config = ConfigDict(str_strip_whitespace=True)

    id: int = Field(gt=0)
    customer_name: str = Field(min_length=1, max_length=100)
    unit_price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    tax_rate: float = Field(default=0.18, ge=0, le=1)


class OrderOut(BaseModel):
    """Datos de salida serializables."""

    id: int
    customer_name: str
    unit_price: float
    quantity: int
    tax_rate: float
    subtotal: float
    tax_amount: float
    total: float
