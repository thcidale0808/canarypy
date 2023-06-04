from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from canarypy.api.dependencies.db import get_db
from canarypy.api.schemas import release
from canarypy.api.schemas.httperror import HTTPError
from canarypy.api.services.release import ReleaseService

router = APIRouter(prefix="", tags=["release"])

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100


@router.post(
    "/release",
    status_code=status.HTTP_201_CREATED,
    response_model=release.ReleaseCreateID,
    summary="Add release",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_release(new_release: release.ReleaseCreate, db: Session = Depends(get_db)):
    print(new_release)
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
    release_service = ReleaseService(db_session=db)

    return release_service.get_latest_release(product_name=product_name)
