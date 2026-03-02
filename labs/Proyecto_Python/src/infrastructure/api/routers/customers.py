"""Router HTTP de clientes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.customers.dto import RegisterCustomerCommand
from src.application.customers.use_cases import ListCustomersUseCase, RegisterCustomerUseCase
from src.infrastructure.api.dependencies import (
    get_list_customers_use_case,
    get_register_customer_use_case,
)
from src.infrastructure.api.schemas.customers import CustomerResponse, RegisterCustomerRequest

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=list[CustomerResponse], status_code=status.HTTP_200_OK)
def list_customers(
    use_case: Annotated[ListCustomersUseCase, Depends(get_list_customers_use_case)],
) -> list[CustomerResponse]:
    """Lista clientes registrados."""
    customers = use_case.execute()
    return [CustomerResponse.from_dto(customer) for customer in customers]


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def register_customer(
    request: RegisterCustomerRequest,
    use_case: Annotated[RegisterCustomerUseCase, Depends(get_register_customer_use_case)],
) -> CustomerResponse:
    """Registra un cliente nuevo."""
    command = RegisterCustomerCommand(
        full_name=request.full_name,
        email=request.email,
    )
    customer_dto = use_case.execute(command)
    return CustomerResponse.from_dto(customer_dto)
