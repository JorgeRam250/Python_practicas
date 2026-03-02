"""Errores tipados para la capa de aplicacion."""

from __future__ import annotations


class ApplicationError(Exception):
    """Error base de aplicacion."""


class ApplicationValidationError(ApplicationError):
    """Error por datos invalidos de entrada o reglas de aplicacion."""


class ApplicationNotFoundError(ApplicationError):
    """Error cuando no se encuentra una entidad requerida."""


class ApplicationConflictError(ApplicationError):
    """Error cuando una operacion entra en conflicto con el estado actual."""


class ApplicationDependencyError(ApplicationError):
    """Error por fallas tecnicas en dependencias externas."""
