from canarypy.api.models.release import Release
from canarypy.api.schemas.release import Release
from sqlalchemy.orm import Session
from uuid import UUID


class ReleaseService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_release_by_id(self, release_id: UUID):
        return self.db_session.query(Release).filter(Release.id == release_id)

    def save(self, release: Release):
        new_release = Release(
            product_id=release.product_id,
            semver_version=release.semver_version
        )
        self.db_session.add(new_release)
        self.db_session.commit()
