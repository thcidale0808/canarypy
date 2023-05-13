from canarypy.api.models.signal import Signal
from canarypy.api.models.release import Release
from canarypy.api.models.product import Product
from sqlalchemy.orm import Session

from canarypy.api.services.release import ReleaseService


class SignalService:

    def __init__(self, db_session: Session, release_service: ReleaseService):
        self.db_session = db_session
        self.release_service = release_service

    def save(self, signal):
        product = self.db_session.query(Product).filter(Product.artifact_url == signal.artifact_url).one_or_none()
        release = self.db_session.query(Release).filter(Release.product_id == product.id, Release.semver_version == signal.semver_version).one_or_none()
        latest_active = self.release_service.get_latest_active_release(product.name)
        latest_canary = self.release_service.get_latest_canary_release(product.name)
        new_signal = Signal(
            release_id=release.id,
            description=signal.description,
            status=signal.status,
            instance_id=signal.instance_id,
        )
        self.db_session.add(new_signal)
        self.db_session.flush()
        if latest_canary and release.id == latest_canary.id:
            release_band = release.active_canary_band
            release_band.canary_executions.append(new_signal)
        elif release.id == latest_active.id and latest_canary:
            release_band = latest_canary.active_canary_band
            release_band.standard_executions.append(new_signal)
        self.db_session.commit()
        return new_signal
