"""Carga datos semilla CSV hacia PostgreSQL transaccional."""

from __future__ import annotations

import asyncio
import csv
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import asyncpg  # type: ignore[import-untyped]

from src.infrastructure.settings import InfrastructureSettings


@dataclass(frozen=True, slots=True)
class CustomerSeedRow:
    """Fila semilla para clientes."""

    customer_id: UUID
    full_name: str
    email: str


@dataclass(frozen=True, slots=True)
class ProductSeedRow:
    """Fila semilla para productos."""

    product_id: UUID
    sku: str
    name: str
    unit_price: Decimal
    is_active: bool


@dataclass(frozen=True, slots=True)
class OrderSeedRow:
    """Fila semilla para ordenes."""

    order_id: UUID
    customer_id: UUID
    branch_id: str
    shipping_cost: Decimal
    tax_rate: Decimal
    status: str
    cancellation_reason: str | None


@dataclass(frozen=True, slots=True)
class OrderItemSeedRow:
    """Fila semilla para lineas de orden."""

    order_id: UUID
    line_number: int
    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int


@dataclass(frozen=True, slots=True)
class InvoiceSeedRow:
    """Fila semilla para facturas externas."""

    order_id: UUID
    external_invoice_id: str
    total_amount: Decimal


@dataclass(frozen=True, slots=True)
class SeedDataset:
    """Conjunto de entidades leidas desde CSV."""

    customers: tuple[CustomerSeedRow, ...]
    products: tuple[ProductSeedRow, ...]
    orders: tuple[OrderSeedRow, ...]
    order_items: tuple[OrderItemSeedRow, ...]
    invoices: tuple[InvoiceSeedRow, ...]


@dataclass(frozen=True, slots=True)
class SeedResult:
    """Resultado de carga semilla a base de datos."""

    inserted_customers: int
    inserted_products: int
    inserted_orders: int
    inserted_order_items: int
    inserted_invoices: int


def _to_asyncpg_dsn(database_url: str) -> str:
    """Convierte URL SQLAlchemy a formato que entiende asyncpg."""
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    if database_url.startswith("postgresql://"):
        return database_url
    raise ValueError("DATABASE_URL invalida. Usa postgresql+asyncpg:// o postgresql://")


def _read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """Lee CSV y regresa filas como diccionarios string."""
    if not csv_path.exists():
        raise FileNotFoundError(f"No existe archivo seed: {csv_path}")
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows: list[dict[str, str]] = []
        for row in reader:
            normalized_row: dict[str, str] = {}
            for key, value in row.items():
                if key is None:
                    continue
                normalized_row[key] = "" if value is None else value
            rows.append(normalized_row)
    return rows


def _as_uuid(value: str) -> UUID:
    """Convierte texto a UUID con error claro."""
    return UUID(value.strip())


def _as_decimal(value: str) -> Decimal:
    """Convierte texto numerico a Decimal."""
    return Decimal(value.strip())


def _as_bool(value: str) -> bool:
    """Convierte texto a booleano aceptando variantes comunes."""
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y", "si", "sí"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Valor booleano invalido: {value}")


def _as_optional_text(value: str) -> str | None:
    """Convierte texto vacio a None."""
    cleaned = value.strip()
    if cleaned == "":
        return None
    return cleaned


def load_seed_dataset(seed_dir: Path) -> SeedDataset:
    """Carga y parsea dataset completo desde data/seed."""
    customer_rows = _read_csv_rows(seed_dir / "customers.csv")
    product_rows = _read_csv_rows(seed_dir / "products.csv")
    order_rows = _read_csv_rows(seed_dir / "orders.csv")
    order_item_rows = _read_csv_rows(seed_dir / "order_items.csv")
    invoice_rows = _read_csv_rows(seed_dir / "invoices.csv")

    customers = tuple(
        CustomerSeedRow(
            customer_id=_as_uuid(row["customer_id"]),
            full_name=row["full_name"].strip(),
            email=row["email"].strip().lower(),
        )
        for row in customer_rows
    )
    products = tuple(
        ProductSeedRow(
            product_id=_as_uuid(row["product_id"]),
            sku=row["sku"].strip(),
            name=row["name"].strip(),
            unit_price=_as_decimal(row["unit_price"]),
            is_active=_as_bool(row["is_active"]),
        )
        for row in product_rows
    )
    orders = tuple(
        OrderSeedRow(
            order_id=_as_uuid(row["order_id"]),
            customer_id=_as_uuid(row["customer_id"]),
            branch_id=row["branch_id"].strip(),
            shipping_cost=_as_decimal(row["shipping_cost"]),
            tax_rate=_as_decimal(row["tax_rate"]),
            status=row["status"].strip(),
            cancellation_reason=_as_optional_text(row["cancellation_reason"]),
        )
        for row in order_rows
    )
    order_items = tuple(
        OrderItemSeedRow(
            order_id=_as_uuid(row["order_id"]),
            line_number=int(row["line_number"].strip()),
            product_id=_as_uuid(row["product_id"]),
            product_name=row["product_name"].strip(),
            unit_price=_as_decimal(row["unit_price"]),
            quantity=int(row["quantity"].strip()),
        )
        for row in order_item_rows
    )
    invoices = tuple(
        InvoiceSeedRow(
            order_id=_as_uuid(row["order_id"]),
            external_invoice_id=row["external_invoice_id"].strip(),
            total_amount=_as_decimal(row["total_amount"]),
        )
        for row in invoice_rows
    )
    return SeedDataset(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        invoices=invoices,
    )


async def _insert_customers(
    connection: asyncpg.Connection, customers: tuple[CustomerSeedRow, ...]
) -> int:
    """Inserta clientes semilla sin duplicar PK."""
    inserted = 0
    for customer in customers:
        result = await connection.execute(
            """
            INSERT INTO customers (customer_id, full_name, email)
            VALUES ($1, $2, $3)
            ON CONFLICT (customer_id) DO NOTHING
            """,
            customer.customer_id,
            customer.full_name,
            customer.email,
        )
        if result.endswith("1"):
            inserted += 1
    return inserted


async def _insert_products(
    connection: asyncpg.Connection, products: tuple[ProductSeedRow, ...]
) -> int:
    """Inserta productos semilla sin duplicar PK."""
    inserted = 0
    for product in products:
        result = await connection.execute(
            """
            INSERT INTO products (product_id, sku, name, unit_price, is_active)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (product_id) DO NOTHING
            """,
            product.product_id,
            product.sku,
            product.name,
            product.unit_price,
            product.is_active,
        )
        if result.endswith("1"):
            inserted += 1
    return inserted


async def _insert_orders(connection: asyncpg.Connection, orders: tuple[OrderSeedRow, ...]) -> int:
    """Inserta ordenes semilla sin duplicar PK."""
    inserted = 0
    for order in orders:
        result = await connection.execute(
            """
            INSERT INTO orders (
                order_id,
                customer_id,
                branch_id,
                shipping_cost,
                tax_rate,
                status,
                cancellation_reason
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (order_id) DO NOTHING
            """,
            order.order_id,
            order.customer_id,
            order.branch_id,
            order.shipping_cost,
            order.tax_rate,
            order.status,
            order.cancellation_reason,
        )
        if result.endswith("1"):
            inserted += 1
    return inserted


async def _insert_order_items(
    connection: asyncpg.Connection, order_items: tuple[OrderItemSeedRow, ...]
) -> int:
    """Inserta lineas de orden semilla sin duplicar PK compuesta."""
    inserted = 0
    for item in order_items:
        result = await connection.execute(
            """
            INSERT INTO order_items (
                order_id,
                line_number,
                product_id,
                product_name,
                unit_price,
                quantity
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (order_id, line_number) DO NOTHING
            """,
            item.order_id,
            item.line_number,
            item.product_id,
            item.product_name,
            item.unit_price,
            item.quantity,
        )
        if result.endswith("1"):
            inserted += 1
    return inserted


async def _insert_invoices(connection: asyncpg.Connection, invoices: tuple[InvoiceSeedRow, ...]) -> int:
    """Inserta facturas semilla sin duplicar PK de orden."""
    inserted = 0
    for invoice in invoices:
        result = await connection.execute(
            """
            INSERT INTO invoice_records (order_id, external_invoice_id, total_amount)
            VALUES ($1, $2, $3)
            ON CONFLICT (order_id) DO NOTHING
            """,
            invoice.order_id,
            invoice.external_invoice_id,
            invoice.total_amount,
        )
        if result.endswith("1"):
            inserted += 1
    return inserted


async def seed_database(database_url: str, seed_dir: Path) -> SeedResult:
    """Carga CSV seed en PostgreSQL dentro de una transaccion."""
    dataset = load_seed_dataset(seed_dir)
    dsn = _to_asyncpg_dsn(database_url)
    connection = await asyncpg.connect(dsn=dsn)
    try:
        async with connection.transaction():
            # Comentario para junior: respetamos dependencias FK, primero padres y luego hijos.
            inserted_customers = await _insert_customers(connection, dataset.customers)
            inserted_products = await _insert_products(connection, dataset.products)
            inserted_orders = await _insert_orders(connection, dataset.orders)
            inserted_order_items = await _insert_order_items(connection, dataset.order_items)
            inserted_invoices = await _insert_invoices(connection, dataset.invoices)
    finally:
        await connection.close()
    return SeedResult(
        inserted_customers=inserted_customers,
        inserted_products=inserted_products,
        inserted_orders=inserted_orders,
        inserted_order_items=inserted_order_items,
        inserted_invoices=inserted_invoices,
    )


def main() -> None:
    """CLI para poblar base transaccional con CSV semilla."""
    settings = InfrastructureSettings.from_env()
    result = asyncio.run(seed_database(settings.database_url, Path("data/seed")))
    print(
        "SEED OK | "
        f"customers={result.inserted_customers} | "
        f"products={result.inserted_products} | "
        f"orders={result.inserted_orders} | "
        f"order_items={result.inserted_order_items} | "
        f"invoices={result.inserted_invoices}"
    )


if __name__ == "__main__":
    main()
