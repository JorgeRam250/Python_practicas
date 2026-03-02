"""Base declarativa para modelos ORM."""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Clase base de todos los modelos ORM."""
