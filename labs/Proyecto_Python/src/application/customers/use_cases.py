"""Casos de uso de clientes."""

from __future__ import annotations

from uuid import uuid4

from src.application.errors import (
    ApplicationConflictError,
    ApplicationDependencyError,
    ApplicationValidationError,
)
from src.application.ports import CustomerRepositoryPort, UnitOfWorkPort
from src.domain.customers.entities import Customer
from src.domain.orders.exceptions import DomainValidationError

from .dto import CustomerDTO, RegisterCustomerCommand


class RegisterCustomerUseCase:
    """Registra un cliente nuevo validando unicidad de email."""

    def __init__(
        self,
        customer_repository: CustomerRepositoryPort,
        unit_of_work: UnitOfWorkPort,
    ) -> None:
        self._customer_repository = customer_repository
        self._unit_of_work = unit_of_work

    def execute(self, command: RegisterCustomerCommand) -> CustomerDTO:
        """Ejecuta el caso de uso de alta de cliente."""
        normalized_email = command.email.strip().lower()
        existing_customer = self._customer_repository.get_by_email(normalized_email)
        if existing_customer is not None:
            raise ApplicationConflictError("Ya existe un cliente registrado con ese email.")

        try:
            customer = Customer(
                customer_id=uuid4(),
                full_name=command.full_name,
                email=normalized_email,
            )
            self._customer_repository.add(customer)
            self._unit_of_work.commit()
            return self._to_dto(customer)
        except DomainValidationError as exc:
            self._unit_of_work.rollback()
            raise ApplicationValidationError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover - proteccion defensiva.
            self._unit_of_work.rollback()
            raise ApplicationDependencyError(
                "No fue posible registrar el cliente por una falla tecnica."
            ) from exc

    @staticmethod
    def _to_dto(customer: Customer) -> CustomerDTO:
        """Mapea entidad de dominio a DTO de salida."""
        return CustomerDTO(
            customer_id=customer.customer_id,
            full_name=customer.full_name,
            email=customer.email,
        )


class ListCustomersUseCase:
    """Lista clientes para consultas de lectura."""

    def __init__(self, customer_repository: CustomerRepositoryPort) -> None:
        self._customer_repository = customer_repository

    def execute(self) -> list[CustomerDTO]:
        """Ejecuta consulta de listado de clientes."""
        customers = self._customer_repository.list()
        return [RegisterCustomerUseCase._to_dto(customer) for customer in customers]
