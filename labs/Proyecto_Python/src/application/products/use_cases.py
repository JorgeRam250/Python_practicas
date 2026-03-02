"""Casos de uso de productos."""

from __future__ import annotations

from uuid import uuid4

from src.application.errors import (
    ApplicationConflictError,
    ApplicationDependencyError,
    ApplicationValidationError,
)
from src.application.ports import ProductRepositoryPort, UnitOfWorkPort
from src.domain.orders.exceptions import DomainValidationError
from src.domain.products.entities import Product

from .dto import CreateProductCommand, ProductDTO


class CreateProductUseCase:
    """Crea un producto para el catalogo operacional."""

    def __init__(
        self,
        product_repository: ProductRepositoryPort,
        unit_of_work: UnitOfWorkPort,
    ) -> None:
        self._product_repository = product_repository
        self._unit_of_work = unit_of_work

    def execute(self, command: CreateProductCommand) -> ProductDTO:
        """Ejecuta el caso de uso de alta de producto."""
        existing_product = self._product_repository.get_by_sku(command.sku.strip())
        if existing_product is not None:
            raise ApplicationConflictError("Ya existe un producto con ese sku.")

        try:
            product = Product(
                product_id=uuid4(),
                sku=command.sku,
                name=command.name,
                unit_price=command.unit_price,
                is_active=command.is_active,
            )
            self._product_repository.add(product)
            self._unit_of_work.commit()
            return self._to_dto(product)
        except DomainValidationError as exc:
            self._unit_of_work.rollback()
            raise ApplicationValidationError(str(exc)) from exc
        except Exception as exc:  # pragma: no cover - proteccion defensiva.
            self._unit_of_work.rollback()
            raise ApplicationDependencyError(
                "No fue posible crear el producto por una falla tecnica."
            ) from exc

    @staticmethod
    def _to_dto(product: Product) -> ProductDTO:
        """Mapea entidad de dominio a DTO de salida."""
        return ProductDTO(
            product_id=product.product_id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            is_active=product.is_active,
        )


class ListProductsUseCase:
    """Lista productos para consultas de lectura."""

    def __init__(self, product_repository: ProductRepositoryPort) -> None:
        self._product_repository = product_repository

    def execute(self) -> list[ProductDTO]:
        """Ejecuta consulta de listado de productos."""
        products = self._product_repository.list()
        return [CreateProductUseCase._to_dto(product) for product in products]
