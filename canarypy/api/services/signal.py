from canarypy.api.models.signal import Signal
from canarypy.api.models.release import Release
from canarypy.api.models.product import Product
from sqlalchemy.orm import Session


class SignalService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, signal):
        product = self.db_session.query(Product).filter(Product.artifact_url == signal.artifact_url).one_or_none()
        release = self.db_session.query(Release).filter(Release.product_id == product.id, Release.semver_version == signal.semver_version).one_or_none()
        new_signal = Signal(
            release_id=release.id,
            description=signal.description,
            status=signal.status,
            instance_id=signal.instance_id
        )
        self.db_session.add(new_signal)
        self.db_session.commit()
