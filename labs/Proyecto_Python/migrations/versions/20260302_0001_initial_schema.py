"""initial schema for distrito chilaquil

Revision ID: 20260302_0001
Revises:
Create Date: 2026-03-02 09:00:00
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260302_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Crea el esquema inicial transaccional."""
    op.create_table(
        "customers",
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("customer_id"),
    )
    op.create_index("ix_customers_email", "customers", ["email"], unique=True)

    op.create_table(
        "products",
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("unit_price >= 0", name="ck_products_unit_price_non_negative"),
        sa.PrimaryKeyConstraint("product_id"),
    )
    op.create_index("ix_products_sku", "products", ["sku"], unique=True)

    op.create_table(
        "orders",
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("branch_id", sa.String(length=100), nullable=False),
        sa.Column("shipping_cost", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("tax_rate", sa.Numeric(precision=5, scale=4), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("cancellation_reason", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("shipping_cost >= 0", name="ck_orders_shipping_non_negative"),
        sa.CheckConstraint("tax_rate >= 0 AND tax_rate <= 1", name="ck_orders_tax_rate_range"),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.customer_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("order_id"),
    )
    op.create_index("ix_orders_branch_id", "orders", ["branch_id"], unique=False)
    op.create_index("ix_orders_customer_id", "orders", ["customer_id"], unique=False)
    op.create_index("ix_orders_status", "orders", ["status"], unique=False)

    op.create_table(
        "order_items",
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("line_number", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Uuid(), nullable=False),
        sa.Column("product_name", sa.String(length=200), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0", name="ck_order_items_unit_price_non_negative"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.order_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("order_id", "line_number"),
    )

    op.create_table(
        "invoice_records",
        sa.Column("order_id", sa.Uuid(), nullable=False),
        sa.Column("external_invoice_id", sa.String(length=100), nullable=False),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("total_amount >= 0", name="ck_invoice_records_total_non_negative"),
        sa.ForeignKeyConstraint(["order_id"], ["orders.order_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("order_id"),
    )
    op.create_index(
        "ix_invoice_records_external_invoice_id",
        "invoice_records",
        ["external_invoice_id"],
        unique=True,
    )


def downgrade() -> None:
    """Revierte el esquema inicial."""
    op.drop_index("ix_invoice_records_external_invoice_id", table_name="invoice_records")
    op.drop_table("invoice_records")

    op.drop_table("order_items")

    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_customer_id", table_name="orders")
    op.drop_index("ix_orders_branch_id", table_name="orders")
    op.drop_table("orders")

    op.drop_index("ix_products_sku", table_name="products")
    op.drop_table("products")

    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_table("customers")
