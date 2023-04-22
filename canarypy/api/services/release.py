from canarypy.api.models.release import Release
from canarypy.api.models.product import Product
from canarypy.api.models.signal import Signal
from sqlalchemy.orm import Session
from uuid import UUID


class ReleaseService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_release_by_id(self, release_id: UUID):
        return self.db_session.query(Release).filter(Release.id == release_id)

    def get_latest_stable_release(self, artifact_url):
        product = self.db_session.query(Product).filter(Product.artifact_url == artifact_url).one_or_none()
        return self.db_session.query(Release).join(Signal).filter(
            Signal.status == 'success', Release.product_id == product.id).order_by(Release.release_date.desc()).first()

    def save(self, release):
        product = self.db_session.query(Product).filter(Product.artifact_url == release.artifact_url).one_or_none()

        new_release = Release(
            product_id=product.id,
            semver_version=release.semver_version
        )
        self.db_session.add(new_release)
        self.db_session.commit()
