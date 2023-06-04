import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from canarypy.api.db.base import Base


class Signal(Base):
    __tablename__ = "signal"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    release_id = Column(UUID(as_uuid=True), ForeignKey(f"release.id"), nullable=False)
    release_canary_band_id = Column(
        UUID(as_uuid=True), ForeignKey(f"release_canary_band.id"), nullable=True
    )
    instance_id = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    status = Column(String(), nullable=False)
    created_date = Column(DateTime, default=func.now())
    release = relationship("canarypy.api.models.release.Release")
    release_canary_band = relationship("canarypy.api.models.release.ReleaseCanaryBand")
    is_canary = Column(Boolean(), default=False, nullable=False)
