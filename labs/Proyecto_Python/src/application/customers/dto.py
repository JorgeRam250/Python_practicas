"""DTOs internos de aplicacion para clientes."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RegisterCustomerCommand:
    """Comando para registrar un cliente."""

    full_name: str
    email: str


@dataclass(frozen=True, slots=True)
class CustomerDTO:
    """Representacion de salida para clientes."""

    customer_id: UUID
    full_name: str
    email: str
