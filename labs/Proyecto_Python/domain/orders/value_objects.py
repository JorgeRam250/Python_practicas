"""Utilidades de validacion y normalizacion para valores de dominio."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from .exceptions import DomainValidationError

ZERO = Decimal("0")
MONEY_SCALE = Decimal("0.01")
TAX_RATE_SCALE = Decimal("0.0001")


def normalize_money(value: Decimal) -> Decimal:
    """Normaliza montos monetarios a 2 decimales."""
    return value.quantize(MONEY_SCALE, rounding=ROUND_HALF_UP)


def validate_non_negative_money(value: Decimal, field_name: str) -> Decimal:
    """Valida que un monto no sea negativo y lo normaliza."""
    if value < ZERO:
        raise DomainValidationError(f"{field_name} debe ser mayor o igual a 0.")
    return normalize_money(value)


def validate_tax_rate(value: Decimal) -> Decimal:
    """Valida la tasa de impuesto en escala decimal [0, 1]."""
    if value < ZERO or value > Decimal("1"):
        raise DomainValidationError("tax_rate debe estar entre 0 y 1 en escala decimal.")
    return value.quantize(TAX_RATE_SCALE, rounding=ROUND_HALF_UP)


def validate_non_empty_text(value: str, field_name: str) -> str:
    """Valida cadenas obligatorias."""
    cleaned_value = value.strip()
    if not cleaned_value:
        raise DomainValidationError(f"{field_name} no puede ser vacio.")
    return cleaned_value


def validate_positive_quantity(value: int) -> int:
    """Valida que la cantidad de items sea positiva."""
    if value <= 0:
        raise DomainValidationError("quantity debe ser mayor a 0.")
    return value
