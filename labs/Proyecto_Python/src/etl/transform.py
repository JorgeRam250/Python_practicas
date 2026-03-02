"""Transformación y validación de datasets ETL."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from src.etl.extract import SeedBatch

MONEY_QUANT = Decimal("0.01")
TAX_QUANT = Decimal("0.0001")


class EtlValidationError(Exception):
    """Error tipado para validaciones de calidad ETL."""


@dataclass(frozen=True, slots=True)
class CustomerRow:
    """Fila tipada de customers."""

    customer_id: UUID
    full_name: str
    email: str


@dataclass(frozen=True, slots=True)
class ProductRow:
    """Fila tipada de products."""

    product_id: UUID
    sku: str
    name: str
    unit_price: Decimal
    is_active: bool


@dataclass(frozen=True, slots=True)
class OrderRow:
    """Fila tipada de orders."""

    order_id: UUID
    customer_id: UUID
    branch_id: str
    shipping_cost: Decimal
    tax_rate: Decimal
    status: str
    cancellation_reason: str | None


@dataclass(frozen=True, slots=True)
class OrderItemRow:
    """Fila tipada de order_items."""

    order_id: UUID
    line_number: int
    product_id: UUID
    product_name: str
    unit_price: Decimal
    quantity: int


@dataclass(frozen=True, slots=True)
class InvoiceRow:
    """Fila tipada de invoices."""

    order_id: UUID
    external_invoice_id: str
    total_amount: Decimal


@dataclass(frozen=True, slots=True)
class TransformedSeed:
    """Dataset ETL transformado con tipos fuertes."""

    customers: list[CustomerRow]
    products: list[ProductRow]
    orders: list[OrderRow]
    order_items: list[OrderItemRow]
    invoices: list[InvoiceRow]


def _as_decimal(value: str, quant: Decimal = MONEY_QUANT) -> Decimal:
    """Convierte texto a Decimal normalizado."""
    return Decimal(value).quantize(quant, rounding=ROUND_HALF_UP)


def _as_tax_rate(value: str) -> Decimal:
    """Convierte texto a tasa decimal [0, 1] con 4 decimales."""
    return Decimal(value).quantize(TAX_QUANT, rounding=ROUND_HALF_UP)


def _as_optional_text(value: str) -> str | None:
    """Normaliza texto opcional."""
    clean_value = value.strip()
    if not clean_value:
        return None
    return clean_value


def transform_seed(batch: SeedBatch) -> TransformedSeed:
    """Transforma CSV crudo a registros tipados."""
    customers = [
        CustomerRow(
            customer_id=UUID(row["customer_id"]),
            full_name=row["full_name"].strip(),
            email=row["email"].strip().lower(),
        )
        for row in batch.customers
    ]
    products = [
        ProductRow(
            product_id=UUID(row["product_id"]),
            sku=row["sku"].strip(),
            name=row["name"].strip(),
            unit_price=_as_decimal(row["unit_price"]),
            is_active=row["is_active"].strip().lower() == "true",
        )
        for row in batch.products
    ]
    orders = [
        OrderRow(
            order_id=UUID(row["order_id"]),
            customer_id=UUID(row["customer_id"]),
            branch_id=row["branch_id"].strip(),
            shipping_cost=_as_decimal(row["shipping_cost"]),
            tax_rate=_as_tax_rate(row["tax_rate"]),
            status=row["status"].strip(),
            cancellation_reason=_as_optional_text(row["cancellation_reason"]),
        )
        for row in batch.orders
    ]
    order_items = [
        OrderItemRow(
            order_id=UUID(row["order_id"]),
            line_number=int(row["line_number"]),
            product_id=UUID(row["product_id"]),
            product_name=row["product_name"].strip(),
            unit_price=_as_decimal(row["unit_price"]),
            quantity=int(row["quantity"]),
        )
        for row in batch.order_items
    ]
    invoices = [
        InvoiceRow(
            order_id=UUID(row["order_id"]),
            external_invoice_id=row["external_invoice_id"].strip(),
            total_amount=_as_decimal(row["total_amount"]),
        )
        for row in batch.invoices
    ]

    return TransformedSeed(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        invoices=invoices,
    )


def validate_record_counts(dataset: TransformedSeed, expected_count: int) -> None:
    """Valida cantidad esperada de registros por entidad principal."""
    if len(dataset.customers) != expected_count:
        raise EtlValidationError("customers no cumple cantidad esperada.")
    if len(dataset.products) != expected_count:
        raise EtlValidationError("products no cumple cantidad esperada.")
    if len(dataset.orders) != expected_count:
        raise EtlValidationError("orders no cumple cantidad esperada.")
    if len(dataset.order_items) != expected_count:
        raise EtlValidationError("order_items no cumple cantidad esperada.")
    if len(dataset.invoices) != expected_count:
        raise EtlValidationError("invoices no cumple cantidad esperada.")


def validate_foreign_keys(dataset: TransformedSeed) -> None:
    """Valida consistencia referencial básica entre tablas CSV."""
    customer_ids = {row.customer_id for row in dataset.customers}
    product_ids = {row.product_id for row in dataset.products}
    order_ids = {row.order_id for row in dataset.orders}

    for order in dataset.orders:
        if order.customer_id not in customer_ids:
            raise EtlValidationError(f"FK invalida: customer_id {order.customer_id} no existe.")

    for item in dataset.order_items:
        if item.order_id not in order_ids:
            raise EtlValidationError(f"FK invalida: order_id {item.order_id} no existe.")
        if item.product_id not in product_ids:
            raise EtlValidationError(f"FK invalida: product_id {item.product_id} no existe.")

    for invoice in dataset.invoices:
        if invoice.order_id not in order_ids:
            raise EtlValidationError(f"FK invalida: invoice.order_id {invoice.order_id} no existe.")


def validate_totals(dataset: TransformedSeed) -> None:
    """Valida coherencia de totales: items + impuestos + shipping = invoice."""
    items_by_order: dict[UUID, list[OrderItemRow]] = {}
    for item in dataset.order_items:
        if item.quantity <= 0:
            raise EtlValidationError("order_items.quantity debe ser mayor a 0.")
        if item.unit_price < Decimal("0"):
            raise EtlValidationError("order_items.unit_price debe ser >= 0.")
        items_by_order.setdefault(item.order_id, []).append(item)

    invoices_by_order = {invoice.order_id: invoice for invoice in dataset.invoices}
    for order in dataset.orders:
        if order.shipping_cost < Decimal("0"):
            raise EtlValidationError("orders.shipping_cost debe ser >= 0.")
        if order.tax_rate < Decimal("0") or order.tax_rate > Decimal("1"):
            raise EtlValidationError("orders.tax_rate debe estar entre 0 y 1.")

        order_items = items_by_order.get(order.order_id, [])
        if not order_items:
            raise EtlValidationError(f"La orden {order.order_id} no tiene items.")

        subtotal = sum(
            (item.unit_price * Decimal(item.quantity) for item in order_items),
            start=Decimal("0"),
        ).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
        tax_total = (subtotal * order.tax_rate).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
        expected_total = (subtotal + tax_total + order.shipping_cost).quantize(
            MONEY_QUANT, rounding=ROUND_HALF_UP
        )

        invoice = invoices_by_order.get(order.order_id)
        if invoice is None:
            raise EtlValidationError(f"La orden {order.order_id} no tiene factura asociada.")
        if invoice.total_amount != expected_total:
            raise EtlValidationError(
                f"Total inconsistente para orden {order.order_id}: "
                f"esperado {expected_total}, recibido {invoice.total_amount}."
            )


def validate_transformed_seed(dataset: TransformedSeed, expected_count: int = 20) -> None:
    """Aplica todas las validaciones ETL del dataset."""
    validate_record_counts(dataset, expected_count=expected_count)
    validate_foreign_keys(dataset)
    validate_totals(dataset)
