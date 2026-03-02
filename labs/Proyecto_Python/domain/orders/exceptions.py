"""Excepciones tipadas para el dominio de ordenes."""

from __future__ import annotations


class DomainError(Exception):
    """Error base para cualquier falla de negocio en el dominio."""


class DomainValidationError(DomainError):
    """Error para invariantes que no se cumplen."""


class InvalidOrderStateTransitionError(DomainError):
    """Error cuando se intenta una transicion de estado invalida."""

    def __init__(self, current_status: str, target_status: str) -> None:
        message = (
            "La transicion de estado no esta permitida: "
            f"{current_status} -> {target_status}."
        )
        super().__init__(message)
        self.current_status = current_status
        self.target_status = target_status
