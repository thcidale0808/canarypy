from fastapi import APIRouter, Depends, HTTPException, Security, status

from canarypy.api.schemas import signal
from canarypy.api.schemas.httperror import HTTPError
from sqlalchemy.orm import Session
from canarypy.api.services.signal import SignalService
from canarypy.api.dependencies.db import get_db


router = APIRouter(prefix="", tags=["signal"])

DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100


@router.post(
    "/signal",
    status_code=status.HTTP_201_CREATED,
    summary="Add signal",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_signal(
    new_signal: signal.Signal,
    db: Session = Depends(get_db)
):
    signal_service = SignalService(db_session=db)

    signal_service.save(new_signal)
