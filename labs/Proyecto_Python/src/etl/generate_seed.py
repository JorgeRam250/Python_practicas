"""Generador determinístico de semillas CSV para ETL."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from uuid import NAMESPACE_DNS, UUID, uuid5

from src.etl.extract import extract_seed
from src.etl.transform import transform_seed, validate_transformed_seed

MONEY_QUANT = Decimal("0.01")
TAX_QUANT = Decimal("0.0001")


@dataclass(frozen=True, slots=True)
class SeedPayload:
    """Payload crudo listo para escribir en CSV."""

    customers: list[dict[str, str]]
    products: list[dict[str, str]]
    orders: list[dict[str, str]]
    order_items: list[dict[str, str]]
    invoices: list[dict[str, str]]


def _stable_uuid(entity: str, index: int) -> UUID:
    """Genera UUID estable para facilitar reproducibilidad."""
    return uuid5(NAMESPACE_DNS, f"distrito-chilaquil-{entity}-{index}")


def _money(value: Decimal) -> str:
    """Formatea Decimal monetario a dos decimales."""
    return str(value.quantize(MONEY_QUANT, rounding=ROUND_HALF_UP))


def _tax(value: Decimal) -> str:
    """Formatea tasa de impuesto a cuatro decimales."""
    return str(value.quantize(TAX_QUANT, rounding=ROUND_HALF_UP))


def build_seed_payload(record_count: int = 20) -> SeedPayload:
    """Construye dataset CSV coherente para ETL."""
    customers: list[dict[str, str]] = []
    products: list[dict[str, str]] = []
    orders: list[dict[str, str]] = []
    order_items: list[dict[str, str]] = []
    invoices: list[dict[str, str]] = []

    for index in range(1, record_count + 1):
        customer_id = _stable_uuid("customer", index)
        product_id = _stable_uuid("product", index)
        order_id = _stable_uuid("order", index)

        tax_rate = Decimal("0.16") if index % 4 != 0 else Decimal("0.08")
        quantity = (index % 3) + 1
        unit_price = Decimal("45.00") + Decimal(index) * Decimal("3.50")
        shipping_cost = Decimal("10.00") + Decimal(index % 5) * Decimal("2.50")

        subtotal = (unit_price * Decimal(quantity)).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
        tax_total = (subtotal * tax_rate).quantize(MONEY_QUANT, rounding=ROUND_HALF_UP)
        total_amount = (subtotal + tax_total + shipping_cost).quantize(
            MONEY_QUANT, rounding=ROUND_HALF_UP
        )

        customers.append(
            {
                "customer_id": str(customer_id),
                "full_name": f"Cliente Seed {index:02d}",
                "email": f"cliente{index:02d}@seed.local",
            }
        )
        products.append(
            {
                "product_id": str(product_id),
                "sku": f"SKU-{index:03d}",
                "name": f"Producto Seed {index:02d}",
                "unit_price": _money(unit_price),
                "is_active": "true",
            }
        )
        orders.append(
            {
                "order_id": str(order_id),
                "customer_id": str(customer_id),
                "branch_id": "CDMX-CENTRO" if index % 2 == 0 else "GDL-CENTRO",
                "shipping_cost": _money(shipping_cost),
                "tax_rate": _tax(tax_rate),
                "status": "COMPLETED",
                "cancellation_reason": "",
            }
        )
        order_items.append(
            {
                "order_id": str(order_id),
                "line_number": "1",
                "product_id": str(product_id),
                "product_name": f"Producto Seed {index:02d}",
                "unit_price": _money(unit_price),
                "quantity": str(quantity),
            }
        )
        invoices.append(
            {
                "order_id": str(order_id),
                "external_invoice_id": f"INV-SEED-{index:04d}",
                "total_amount": _money(total_amount),
            }
        )

    return SeedPayload(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        invoices=invoices,
    )


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Escribe un archivo CSV a partir de filas homogéneas."""
    if not rows:
        raise ValueError(f"No hay filas para escribir en {path}.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_seed_files(payload: SeedPayload, seed_dir: Path) -> None:
    """Persiste payload en `data/seed`."""
    _write_csv(seed_dir / "customers.csv", payload.customers)
    _write_csv(seed_dir / "products.csv", payload.products)
    _write_csv(seed_dir / "orders.csv", payload.orders)
    _write_csv(seed_dir / "order_items.csv", payload.order_items)
    _write_csv(seed_dir / "invoices.csv", payload.invoices)


def generate_and_validate(seed_dir: Path, record_count: int = 20) -> SeedPayload:
    """Genera archivos seed y valida coherencia referencial + totales."""
    payload = build_seed_payload(record_count=record_count)
    write_seed_files(payload=payload, seed_dir=seed_dir)

    # Validación de extremo a extremo usando el pipeline de transformaciones.
    extracted = extract_seed(seed_dir=seed_dir)
    transformed = transform_seed(batch=extracted)
    validate_transformed_seed(transformed, expected_count=record_count)
    return payload


def main() -> None:
    """CLI para generar seeds coherentes."""
    seed_dir = Path("data/seed")
    generate_and_validate(seed_dir=seed_dir, record_count=20)
    print(f"Seeds generadas correctamente en {seed_dir}.")


if __name__ == "__main__":
    main()
