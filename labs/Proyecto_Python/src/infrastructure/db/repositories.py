"""Repositorios concretos SQLAlchemy que implementan puertos de aplicacion."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.ports import (
    CustomerRepositoryPort,
    InvoiceRecord,
    InvoiceRepositoryPort,
    OrderRepositoryPort,
    ProductRepositoryPort,
)
from src.domain.customers.entities import Customer
from src.domain.orders.entities import Order, OrderStatus
from src.domain.products.entities import Product
from src.infrastructure.common.async_runner import run_sync

from .mappers import (
    to_customer_domain,
    to_customer_model,
    to_invoice_record_domain,
    to_invoice_record_model,
    to_order_domain,
    to_order_model,
    to_product_domain,
    to_product_model,
)
from .models import CustomerModel, InvoiceRecordModel, OrderItemModel, OrderModel, ProductModel


class SqlAlchemyCustomerRepository(CustomerRepositoryPort):
    """Repositorio concreto de clientes."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, customer: Customer) -> None:
        model = to_customer_model(customer)
        self._session.add(model)
        run_sync(self._session.flush())

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        statement: Select[tuple[CustomerModel]] = select(CustomerModel).where(
            CustomerModel.customer_id == customer_id
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_customer_domain(model)

    def get_by_email(self, email: str) -> Customer | None:
        normalized_email = email.strip().lower()
        statement: Select[tuple[CustomerModel]] = select(CustomerModel).where(
            CustomerModel.email == normalized_email
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_customer_domain(model)

    def list(self) -> list[Customer]:
        statement: Select[tuple[CustomerModel]] = select(CustomerModel).order_by(
            CustomerModel.created_at.asc()
        )
        result = run_sync(self._session.execute(statement))
        models = result.scalars().all()
        return [to_customer_domain(model) for model in models]


class SqlAlchemyProductRepository(ProductRepositoryPort):
    """Repositorio concreto de productos."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, product: Product) -> None:
        model = to_product_model(product)
        self._session.add(model)
        run_sync(self._session.flush())

    def get_by_id(self, product_id: UUID) -> Product | None:
        statement: Select[tuple[ProductModel]] = select(ProductModel).where(
            ProductModel.product_id == product_id
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_product_domain(model)

    def get_by_sku(self, sku: str) -> Product | None:
        normalized_sku = sku.strip()
        statement: Select[tuple[ProductModel]] = select(ProductModel).where(
            ProductModel.sku == normalized_sku
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_product_domain(model)

    def list(self) -> list[Product]:
        statement: Select[tuple[ProductModel]] = select(ProductModel).order_by(
            ProductModel.created_at.asc()
        )
        result = run_sync(self._session.execute(statement))
        models = result.scalars().all()
        return [to_product_domain(model) for model in models]


class SqlAlchemyOrderRepository(OrderRepositoryPort):
    """Repositorio concreto de ordenes."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, order: Order) -> None:
        model = to_order_model(order)
        self._session.add(model)
        run_sync(self._session.flush())

    def update(self, order: Order) -> None:
        statement: Select[tuple[OrderModel]] = (
            select(OrderModel)
            .options(selectinload(OrderModel.customer), selectinload(OrderModel.items))
            .where(OrderModel.order_id == order.order_id)
        )
        result = run_sync(self._session.execute(statement))
        existing = result.scalar_one_or_none()
        if existing is None:
            raise LookupError(f"No existe orden para actualizar: {order.order_id}.")

        existing.branch_id = order.branch_id
        existing.shipping_cost = order.shipping_cost
        existing.tax_rate = order.tax_rate
        existing.status = order.status.value
        existing.cancellation_reason = order.cancellation_reason
        # Comentario para junior: se reconstruyen lineas sin crear un OrderModel nuevo.
        existing.items = [
            OrderItemModel(
                order_id=order.order_id,
                line_number=index,
                product_id=item.product_id,
                product_name=item.product_name,
                unit_price=item.unit_price,
                quantity=item.quantity,
            )
            for index, item in enumerate(order.items, start=1)
        ]
        run_sync(self._session.flush())

    def get_by_id(self, order_id: UUID) -> Order | None:
        statement: Select[tuple[OrderModel]] = (
            select(OrderModel)
            .options(selectinload(OrderModel.customer), selectinload(OrderModel.items))
            .where(OrderModel.order_id == order_id)
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_order_domain(model)

    def list(self, status: OrderStatus | None = None) -> list[Order]:
        statement: Select[tuple[OrderModel]] = select(OrderModel).options(
            selectinload(OrderModel.customer),
            selectinload(OrderModel.items),
        )
        if status is not None:
            statement = statement.where(OrderModel.status == status.value)

        result = run_sync(self._session.execute(statement.order_by(OrderModel.created_at.asc())))
        models = result.scalars().all()
        return [to_order_domain(model) for model in models]


class SqlAlchemyInvoiceRepository(InvoiceRepositoryPort):
    """Repositorio concreto de registros de facturas externas."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, record: InvoiceRecord) -> None:
        model = to_invoice_record_model(record)
        self._session.add(model)
        run_sync(self._session.flush())

    def get_by_order_id(self, order_id: UUID) -> InvoiceRecord | None:
        statement: Select[tuple[InvoiceRecordModel]] = select(InvoiceRecordModel).where(
            InvoiceRecordModel.order_id == order_id
        )
        result = run_sync(self._session.execute(statement))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return to_invoice_record_domain(model)
