from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from canarypy.api.dependencies.db import get_db
from canarypy.api.schemas import release
from canarypy.api.schemas.httperror import HTTPError
from canarypy.api.services.release import ReleaseService

router = APIRouter(prefix="", tags=["release"])


@router.post(
    "/release",
    status_code=status.HTTP_201_CREATED,
    response_model=release.ReleaseCreateID,
    summary="Add release",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_release(new_release: release.ReleaseCreate, db: Session = Depends(get_db)):
    """Add a new release to the database.

    Parameters:
    new_release (release.ReleaseCreate): The release to add.
    db (Session): The database session to use.

    Returns:
    release.ReleaseCreateID: The added release object with its ID.
    """
    release_service = ReleaseService(db_session=db)
    return release_service.save(new_release)


@router.get(
    "/release/{product_name}/latest",
    response_model=release.Release,
    status_code=status.HTTP_200_OK,
    summary="Get Release",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def get_latest_release(product_name: str, db: Session = Depends(get_db)):
    """Get the latest release of the specified product.

    Parameters:
    product_name (str): The name of the product to get the latest release for.
    db (Session): The database session to use.

    Returns:
    release.Release: The latest release object of the specified product.
    """
    release_service = ReleaseService(db_session=db)
    return release_service.get_latest_release(product_name=product_name)
