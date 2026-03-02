"""Modelos ORM de infraestructura para PostgreSQL."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class CustomerModel(Base):
    """Tabla de clientes."""

    __tablename__ = "customers"

    customer_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    orders: Mapped[list[OrderModel]] = relationship(back_populates="customer")


class ProductModel(Base):
    """Tabla de productos."""

    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("unit_price >= 0", name="ck_products_unit_price_non_negative"),
    )

    product_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class OrderModel(Base):
    """Tabla de ordenes."""

    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("shipping_cost >= 0", name="ck_orders_shipping_non_negative"),
        CheckConstraint("tax_rate >= 0 AND tax_rate <= 1", name="ck_orders_tax_rate_range"),
    )

    order_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    customer_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("customers.customer_id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    branch_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    shipping_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=Decimal("0"))
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False, default=Decimal("0.16"))
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    cancellation_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    customer: Mapped[CustomerModel] = relationship(back_populates="orders")
    items: Mapped[list[OrderItemModel]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderItemModel.line_number",
    )


class OrderItemModel(Base):
    """Tabla de lineas de orden."""

    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_order_items_unit_price_non_negative"),
    )

    order_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        primary_key=True,
    )
    line_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    product_name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped[OrderModel] = relationship(back_populates="items")


class InvoiceRecordModel(Base):
    """Tabla de registros de factura externa."""

    __tablename__ = "invoice_records"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_invoice_records_total_non_negative"),
    )

    order_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        primary_key=True,
    )
    external_invoice_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
