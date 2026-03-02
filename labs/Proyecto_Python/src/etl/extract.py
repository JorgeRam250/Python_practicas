"""Funciones de extracción para datasets CSV del ETL."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SeedBatch:
    """Contenedor de datos crudos extraídos desde CSV."""

    customers: list[dict[str, str]]
    products: list[dict[str, str]]
    orders: list[dict[str, str]]
    order_items: list[dict[str, str]]
    invoices: list[dict[str, str]]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Lee un CSV y devuelve filas como diccionarios de strings."""
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo requerido: {path}")
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def extract_seed(seed_dir: Path) -> SeedBatch:
    """Extrae lote de seeds desde el directorio objetivo."""
    # La extracción se mantiene desacoplada del dominio transaccional.
    customers = read_csv_rows(seed_dir / "customers.csv")
    products = read_csv_rows(seed_dir / "products.csv")
    orders = read_csv_rows(seed_dir / "orders.csv")
    order_items = read_csv_rows(seed_dir / "order_items.csv")
    invoices = read_csv_rows(seed_dir / "invoices.csv")
    return SeedBatch(
        customers=customers,
        products=products,
        orders=orders,
        order_items=order_items,
        invoices=invoices,
    )
