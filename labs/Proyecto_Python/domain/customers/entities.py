"""Entidades del subdominio de clientes."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.domain.orders.exceptions import DomainValidationError
from src.domain.orders.value_objects import validate_non_empty_text


@dataclass(frozen=True, slots=True)
class Customer:
    """Entidad cliente usada por el agregado de orden."""

    customer_id: UUID
    full_name: str
    email: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "full_name", validate_non_empty_text(self.full_name, "full_name"))
        cleaned_email = validate_non_empty_text(self.email, "email").lower()

        # Validacion simple para mantener el dominio agnostico a librerias externas.
        if "@" not in cleaned_email:
            raise DomainValidationError("email debe contener '@'.")

        local_part, _, domain_part = cleaned_email.partition("@")
        if not local_part or "." not in domain_part:
            raise DomainValidationError("email no tiene un formato valido.")

        object.__setattr__(self, "email", cleaned_email)
