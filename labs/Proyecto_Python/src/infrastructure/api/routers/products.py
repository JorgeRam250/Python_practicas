"""Router HTTP de productos."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.products.dto import CreateProductCommand
from src.application.products.use_cases import CreateProductUseCase, ListProductsUseCase
from src.infrastructure.api.dependencies import (
    get_create_product_use_case,
    get_list_products_use_case,
)
from src.infrastructure.api.schemas.products import CreateProductRequest, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def list_products(
    use_case: Annotated[ListProductsUseCase, Depends(get_list_products_use_case)],
) -> list[ProductResponse]:
    """Lista productos disponibles en catalogo."""
    products = use_case.execute()
    return [ProductResponse.from_dto(product) for product in products]


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    request: CreateProductRequest,
    use_case: Annotated[CreateProductUseCase, Depends(get_create_product_use_case)],
) -> ProductResponse:
    """Crea un producto del catalogo."""
    command = CreateProductCommand(
        sku=request.sku,
        name=request.name,
        unit_price=request.unit_price,
        is_active=request.is_active,
    )
    product_dto = use_case.execute(command)
    return ProductResponse.from_dto(product_dto)
