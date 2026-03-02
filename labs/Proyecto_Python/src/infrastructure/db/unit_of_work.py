"""Unidad de trabajo concreta sobre AsyncSession."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports import UnitOfWorkPort
from src.infrastructure.common.async_runner import run_sync


class SqlAlchemyUnitOfWork(UnitOfWorkPort):
    """Implementacion de UnitOfWork para puertos sincronos."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """Expone la sesion para construir repositorios concretos."""
        return self._session

    def commit(self) -> None:
        run_sync(self._session.commit())

    def rollback(self) -> None:
        run_sync(self._session.rollback())

    def close(self) -> None:
        """Cierra recursos de sesion."""
        run_sync(self._session.close())
