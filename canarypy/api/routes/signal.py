from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from canarypy.api.dependencies.db import get_db
from canarypy.api.schemas import signal
from canarypy.api.schemas.httperror import HTTPError
from canarypy.api.services.release import ReleaseService
from canarypy.api.services.signal import SignalService

router = APIRouter(prefix="", tags=["signal"])


@router.post(
    "/signal",
    status_code=status.HTTP_201_CREATED,
    summary="Add signal",
    responses={400: {"model": HTTPError}, 403: {"model": HTTPError}},
)
def add_signal(new_signal: signal.Signal, db: Session = Depends(get_db)):
    """Add a new signal to the database.

    Parameters:
    new_signal (signal.Signal): The signal to add.
    db (Session): The database session to use.

    Returns:
    None: This function does not return anything.
    """
    signal_service = SignalService(
        db_session=db, release_service=ReleaseService(db_session=db)
    )
    signal_service.save(new_signal)
