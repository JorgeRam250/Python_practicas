"""Schemas API para clientes."""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from src.application.customers.dto import CustomerDTO

from .common import ApiBaseModel


class RegisterCustomerRequest(ApiBaseModel):
    """Payload de alta de cliente."""

    full_name: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=3, max_length=320)


class CustomerResponse(ApiBaseModel):
    """Respuesta HTTP de cliente."""

    customer_id: UUID
    full_name: str
    email: str

    @classmethod
    def from_dto(cls, dto: CustomerDTO) -> CustomerResponse:
        """Mapea DTO de aplicacion a schema de respuesta."""
        return cls(
            customer_id=dto.customer_id,
            full_name=dto.full_name,
            email=dto.email,
        )
