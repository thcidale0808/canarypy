from fastapi import APIRouter, Depends, HTTPException, Security, status
from canarypy.api.schemas import release
from canarypy.api.schemas.httperror import HTTPError
from sqlalchemy.orm import Session
from canarypy.api.services.release import ReleaseService
from canarypy.api.dependencies.db import get_db

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
    new_release: release.ReleaseCreate,
    db: Session = Depends(get_db)
):
    print(new_release)
    release_service = ReleaseService(db_session=db)

    release_service.save(new_release)


@router.get(
    "/release/{artifact_url}/latest",
    response_model=release.Release,
    status_code=status.HTTP_200_OK,
    summary="Get Release",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def get_latest_release(
    artifact_url: str,
    db: Session = Depends(get_db)
):
    release_service = ReleaseService(db_session=db)

    return release_service.get_latest_stable_release(artifact_url=artifact_url)
