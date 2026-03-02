"""Wiring de dependencias API hacia aplicacion e infraestructura."""

from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from typing import Annotated, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.application.customers.use_cases import ListCustomersUseCase, RegisterCustomerUseCase
from src.application.orders.use_cases import (
    CreateOrderUseCase,
    GetOrderUseCase,
    ListOrdersUseCase,
    UpdateOrderStatusUseCase,
)
from src.application.ports import (
    CustomerRepositoryPort,
    EventPublisherPort,
    OrderRepositoryPort,
    ProductRepositoryPort,
    UnitOfWorkPort,
)
from src.application.products.use_cases import CreateProductUseCase, ListProductsUseCase
from src.infrastructure.common.async_runner import run_sync
from src.infrastructure.db.repositories import (
    SqlAlchemyCustomerRepository,
    SqlAlchemyOrderRepository,
    SqlAlchemyProductRepository,
)
from src.infrastructure.db.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.events.kafka_publisher import AIOKafkaEventPublisher
from src.infrastructure.settings import InfrastructureSettings


@dataclass(frozen=True, slots=True)
class ApiContainer:
    """Contenedor de infraestructura compartido por la API."""

    settings: InfrastructureSettings
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    event_publisher: AIOKafkaEventPublisher


def get_container(request: Request) -> ApiContainer:
    """Obtiene el contenedor desde el estado de la aplicacion."""
    return cast(ApiContainer, request.app.state.container)


def get_db_session(
    container: Annotated[ApiContainer, Depends(get_container)],
) -> Generator[AsyncSession, None, None]:
    """Abre/cierra sesion SQLAlchemy por request.

    La dependencia es sincrona para ser compatible con puertos sincronos actuales.
    """
    session = container.session_factory()
    try:
        yield session
    finally:
        run_sync(session.close())


def get_customer_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CustomerRepositoryPort:
    """Entrega repositorio concreto de clientes."""
    return SqlAlchemyCustomerRepository(session)


def get_product_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProductRepositoryPort:
    """Entrega repositorio concreto de productos."""
    return SqlAlchemyProductRepository(session)


def get_order_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> OrderRepositoryPort:
    """Entrega repositorio concreto de ordenes."""
    return SqlAlchemyOrderRepository(session)


def get_unit_of_work(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UnitOfWorkPort:
    """Entrega UnitOfWork concreto."""
    return SqlAlchemyUnitOfWork(session)


def get_event_publisher(
    container: Annotated[ApiContainer, Depends(get_container)],
) -> EventPublisherPort:
    """Entrega publicador de eventos."""
    return container.event_publisher


def get_register_customer_use_case(
    customer_repository: Annotated[CustomerRepositoryPort, Depends(get_customer_repository)],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> RegisterCustomerUseCase:
    """Construye caso de uso RegisterCustomer."""
    return RegisterCustomerUseCase(
        customer_repository=customer_repository,
        unit_of_work=unit_of_work,
    )


def get_list_customers_use_case(
    customer_repository: Annotated[CustomerRepositoryPort, Depends(get_customer_repository)],
) -> ListCustomersUseCase:
    """Construye caso de uso ListCustomers."""
    return ListCustomersUseCase(customer_repository=customer_repository)


def get_create_product_use_case(
    product_repository: Annotated[ProductRepositoryPort, Depends(get_product_repository)],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> CreateProductUseCase:
    """Construye caso de uso CreateProduct."""
    return CreateProductUseCase(
        product_repository=product_repository,
        unit_of_work=unit_of_work,
    )


def get_list_products_use_case(
    product_repository: Annotated[ProductRepositoryPort, Depends(get_product_repository)],
) -> ListProductsUseCase:
    """Construye caso de uso ListProducts."""
    return ListProductsUseCase(product_repository=product_repository)


def get_create_order_use_case(
    customer_repository: Annotated[CustomerRepositoryPort, Depends(get_customer_repository)],
    product_repository: Annotated[ProductRepositoryPort, Depends(get_product_repository)],
    order_repository: Annotated[OrderRepositoryPort, Depends(get_order_repository)],
    event_publisher: Annotated[EventPublisherPort, Depends(get_event_publisher)],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> CreateOrderUseCase:
    """Construye caso de uso CreateOrder."""
    return CreateOrderUseCase(
        customer_repository=customer_repository,
        product_repository=product_repository,
        order_repository=order_repository,
        event_publisher=event_publisher,
        unit_of_work=unit_of_work,
    )


def get_get_order_use_case(
    order_repository: Annotated[OrderRepositoryPort, Depends(get_order_repository)],
) -> GetOrderUseCase:
    """Construye caso de uso GetOrder."""
    return GetOrderUseCase(order_repository=order_repository)


def get_list_orders_use_case(
    order_repository: Annotated[OrderRepositoryPort, Depends(get_order_repository)],
) -> ListOrdersUseCase:
    """Construye caso de uso ListOrders."""
    return ListOrdersUseCase(order_repository=order_repository)


def get_update_order_status_use_case(
    order_repository: Annotated[OrderRepositoryPort, Depends(get_order_repository)],
    event_publisher: Annotated[EventPublisherPort, Depends(get_event_publisher)],
    unit_of_work: Annotated[UnitOfWorkPort, Depends(get_unit_of_work)],
) -> UpdateOrderStatusUseCase:
    """Construye caso de uso UpdateOrderStatus."""
    return UpdateOrderStatusUseCase(
        order_repository=order_repository,
        event_publisher=event_publisher,
        unit_of_work=unit_of_work,
    )
