"""Carga de datos ETL transformados hacia archivos staging."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from src.etl.transform import TransformedSeed


@dataclass(frozen=True, slots=True)
class LoadResult:
    """Resultado de la carga a staging."""

    output_dir: Path
    files_written: tuple[Path, ...]


def _write_dict_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    """Escribe filas en CSV manteniendo encabezados del primer registro."""
    if not rows:
        raise ValueError(f"No hay filas para escribir en {path}.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_to_staging(dataset: TransformedSeed, output_dir: Path) -> LoadResult:
    """Carga dataset validado a directorio staging en formato CSV."""
    customers_path = output_dir / "customers_staging.csv"
    products_path = output_dir / "products_staging.csv"
    orders_path = output_dir / "orders_staging.csv"
    order_items_path = output_dir / "order_items_staging.csv"
    invoices_path = output_dir / "invoices_staging.csv"

    _write_dict_rows(customers_path, [asdict(row) for row in dataset.customers])
    _write_dict_rows(products_path, [asdict(row) for row in dataset.products])
    _write_dict_rows(orders_path, [asdict(row) for row in dataset.orders])
    _write_dict_rows(order_items_path, [asdict(row) for row in dataset.order_items])
    _write_dict_rows(invoices_path, [asdict(row) for row in dataset.invoices])

    return LoadResult(
        output_dir=output_dir,
        files_written=(
            customers_path,
            products_path,
            orders_path,
            order_items_path,
            invoices_path,
        ),
    )
