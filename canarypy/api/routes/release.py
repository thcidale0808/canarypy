from fastapi import APIRouter, Depends, HTTPException, Security, status
from canarypy.api.schemas import release
from canarypy.api.schemas.httperror import HTTPError
from sqlalchemy.orm import Session
from canarypy.api.services.release import ReleaseService
from canarypy.api.dependencies.db import get_db
from uuid import UUID

router = APIRouter(prefix="", tags=["release"])

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100


@router.post(
    "/release",
    status_code=status.HTTP_201_CREATED,
    summary="Add release",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_release(
    new_release: release.Release,
    db: Session = Depends(get_db)
):
    release_service = ReleaseService(db_session=db)

    release_service.save(new_release)


@router.get(
    "/release/{id}",
    response_model=release.Release,
    status_code=status.HTTP_200_OK,
    summary="Get Developer",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def get_release_by_id(
    id: UUID,
    db: Session = Depends(get_db)
):
    release_service = ReleaseService(db_session=db)

    return release_service.get_release_by_id(id)
