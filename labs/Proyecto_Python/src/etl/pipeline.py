"""Pipeline ETL para datasets seed CSV."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.etl.extract import extract_seed
from src.etl.load import load_to_staging
from src.etl.transform import transform_seed, validate_transformed_seed


@dataclass(frozen=True, slots=True)
class PipelineSummary:
    """Resumen de ejecución del pipeline ETL."""

    seed_dir: Path
    staging_dir: Path
    records_per_entity: int


def run_pipeline(seed_dir: Path, staging_dir: Path, expected_count: int = 20) -> PipelineSummary:
    """Ejecuta pipeline ETL completo: extract -> transform -> validate -> load."""
    extracted = extract_seed(seed_dir=seed_dir)
    transformed = transform_seed(batch=extracted)
    validate_transformed_seed(transformed, expected_count=expected_count)
    load_to_staging(dataset=transformed, output_dir=staging_dir)
    return PipelineSummary(
        seed_dir=seed_dir,
        staging_dir=staging_dir,
        records_per_entity=expected_count,
    )


def main() -> None:
    """Punto de entrada CLI del pipeline ETL."""
    seed_dir = Path("data/seed")
    staging_dir = Path("data/staging")
    summary = run_pipeline(seed_dir=seed_dir, staging_dir=staging_dir, expected_count=20)
    print(
        "ETL OK | "
        f"seed_dir={summary.seed_dir} | "
        f"staging_dir={summary.staging_dir} | "
        f"records_per_entity={summary.records_per_entity}"
    )


if __name__ == "__main__":
    main()
