import datetime

from sqlalchemy.orm import Session

from canarypy.api.models.product import Product
from canarypy.api.models.release import Release
from canarypy.api.models.signal import Signal
from canarypy.api.schemas import signal as signal_schema
from canarypy.api.services.release import ReleaseService


class SignalService:
    """Service class for handling operations related to Signal.

    Attributes:
    db_session (Session): Database session to interact with the database.
    release_service (ReleaseService): Service to handle operations related to Release.
    """

    def __init__(self, db_session: Session, release_service: ReleaseService):
        """Initialize SignalService with the database session and release service.

        Parameters:
        db_session (Session): Database session to interact with the database.
        release_service (ReleaseService): Service to handle operations related to Release.
        """
        self.db_session = db_session
        self.release_service = release_service

    def save(self, signal: signal_schema.Signal):
        """Save a new Signal to the database. The method also checks if the release
        associated with the signal is the latest canary release or the latest active
        release and adjusts the 'is_canary' flag and 'release_canary_band_id' field of
        the signal accordingly.

        Parameters:
        signal (Signal): The Signal to save.

        Returns:
        Signal: The newly saved Signal object.
        """
        product = (
            self.db_session.query(Product)
            .filter(Product.artifact_url == signal.artifact_url)
            .one_or_none()
        )
        release = (
            self.db_session.query(Release)
            .filter(
                Release.product_id == product.id,
                Release.semver_version == signal.semver_version,
            )
            .one_or_none()
        )
        latest_canary = self.release_service.get_latest_canary_release(product.name)
        latest_active = self.release_service.get_latest_active_release(product.name)
        if latest_canary and release.id == latest_canary.id:
            release_band = release.active_canary_band
            new_signal = Signal(
                release_id=release.id,
                description=signal.description,
                status=signal.status,
                instance_id=signal.instance_id,
                release_canary_band_id=release_band.id,
                created_date=datetime.datetime.now(),
                is_canary=True,
            )
            self.db_session.add(new_signal)
            self.db_session.flush()
        elif latest_canary and release.id == latest_active.id:
            release_band = latest_canary.active_canary_band
            new_signal = Signal(
                release_id=release.id,
                description=signal.description,
                status=signal.status,
                instance_id=signal.instance_id,
                release_canary_band_id=release_band.id,
                created_date=datetime.datetime.now(),
                is_canary=False,
            )
            self.db_session.add(new_signal)
            self.db_session.flush()
        else:
            new_signal = Signal(
                release_id=release.id,
                description=signal.description,
                status=signal.status,
                instance_id=signal.instance_id,
                created_date=datetime.datetime.now(),
                is_canary=False,
            )
            self.db_session.add(new_signal)
            self.db_session.flush()
        self.db_session.commit()
        return new_signal
