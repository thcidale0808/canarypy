from fastapi import APIRouter, Depends, status
from typing import List
from canarypy.api.schemas import product
from canarypy.api.schemas.httperror import HTTPError
from sqlalchemy.orm import Session
from canarypy.api.services.product import ProductService
from canarypy.api.dependencies.db import get_db
from uuid import UUID

router = APIRouter(prefix="", tags=["product"])

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100


@router.get(
    "/product",
    response_model=List[product.Product],
    summary="Show a list of products",
    response_description="List of products",
    responses={403: {"model": HTTPError}},
)
def list_products(
    db: Session = Depends(get_db)
) -> List[product.Product]:

    product_service = ProductService(db_session=db)

    product = product_service.get_products()

    return product


@router.post(
    "/product",
    response_model=product.Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add product",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_product(
    new_product: product.Product,
    db: Session = Depends(get_db)
):
    product_service = ProductService(db_session=db)

    return product_service.save(new_product)


@router.get(
    "/product/{id}",
    response_model=product.Product,
    status_code=status.HTTP_200_OK,
    summary="Get Product",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def get_product_by_id(
    id: UUID,
    db: Session = Depends(get_db)
):
    product_service = ProductService(db_session=db)
    response = product_service.get_product_by_id(id)
    return response
