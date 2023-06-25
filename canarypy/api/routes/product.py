from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from canarypy.api.dependencies.db import get_db
from canarypy.api.schemas import product
from canarypy.api.schemas.httperror import HTTPError
from canarypy.api.services.product import ProductService

router = APIRouter(prefix="", tags=["product"])


@router.get(
    "/product",
    response_model=List[product.Product],
    summary="Show a list of products",
    response_description="List of products",
    responses={403: {"model": HTTPError}},
)
def list_products(db: Session = Depends(get_db)) -> List[product.Product]:
    """Return a list of all products.

    Parameters:
    db (Session): The database session to use.

    Returns:
    List[product.Product]: A list of product objects.
    """
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
def add_product(new_product: product.Product, db: Session = Depends(get_db)):
    """Add a new product to the database.

    Parameters:
    new_product (product.Product): The product to add.
    db (Session): The database session to use.

    Returns:
    product.Product: The added product object.
    """
    product_service = ProductService(db_session=db)

    return product_service.save(new_product)


@router.get(
    "/product/{id}",
    response_model=product.Product,
    status_code=status.HTTP_200_OK,
    summary="Get Product",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def get_product_by_id(id: UUID, db: Session = Depends(get_db)):
    """Return the product with the specified ID.

    Parameters:
    id (UUID): The ID of the product to return.
    db (Session): The database session to use.

    Returns:
    product.Product: The product object.
    """
    product_service = ProductService(db_session=db)
    response = product_service.get_product_by_id(id)
    return response
