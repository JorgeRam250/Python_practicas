"""Router HTTP de ordenes."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from src.application.orders.dto import (
    CreateOrderCommand,
    CreateOrderItemInput,
    GetOrderQuery,
    ListOrdersQuery,
    UpdateOrderStatusCommand,
)
from src.application.orders.use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    UpdateOrderStatusUseCase,
)
from src.infrastructure.api.dependencies import (
    get_create_order_use_case,
    get_get_order_use_case,
    get_list_orders_use_case,
    get_update_order_status_use_case,
)
from src.infrastructure.api.schemas.orders import (
    CreateOrderRequest,
    OrderResponse,
    OrderStatusEnum,
    UpdateOrderStatusRequest,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)],
) -> OrderResponse:
    """Crea una orden."""
    command = CreateOrderCommand(
        customer_id=request.customer_id,
        branch_id=request.branch_id,
        items=tuple(
            CreateOrderItemInput(product_id=item.product_id, quantity=item.quantity)
            for item in request.items
        ),
        shipping_cost=request.shipping_cost,
        tax_rate=request.tax_rate,
    )
    order_dto = use_case.execute(command)
    return OrderResponse.from_dto(order_dto)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: UUID,
    use_case: Annotated[GetOrderUseCase, Depends(get_get_order_use_case)],
) -> OrderResponse:
    """Consulta una orden por id."""
    order_dto = use_case.execute(GetOrderQuery(order_id=order_id))
    return OrderResponse.from_dto(order_dto)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    use_case: Annotated[ListOrdersUseCase, Depends(get_list_orders_use_case)],
    status_filter: Annotated[OrderStatusEnum | None, Query(alias="status")] = None,
) -> list[OrderResponse]:
    """Lista ordenes con filtro opcional por estado."""
    status = status_filter.to_domain() if status_filter is not None else None
    order_dtos = use_case.execute(ListOrdersQuery(status=status))
    return [OrderResponse.from_dto(order_dto) for order_dto in order_dtos]


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: UUID,
    request: UpdateOrderStatusRequest,
    use_case: Annotated[UpdateOrderStatusUseCase, Depends(get_update_order_status_use_case)],
) -> OrderResponse:
    """Actualiza estado de una orden."""
    command = UpdateOrderStatusCommand(
        order_id=order_id,
        target_status=request.target_status.to_domain(),
        cancellation_reason=request.cancellation_reason,
    )
    order_dto = use_case.execute(command)
    return OrderResponse.from_dto(order_dto)
