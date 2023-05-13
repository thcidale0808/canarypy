from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Boolean,
    Numeric,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from canarypy.api.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime


class Release(Base):
    __tablename__ = "release"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    product_id = Column(
        UUID(as_uuid=True), ForeignKey(f"product.id"), nullable=False
    )
    semver_version = Column(String(), nullable=True)
    product = relationship("canarypy.api.models.product.Product")
    release_date = Column(DateTime, default=func.now())
    is_canary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    threshold = Column(Numeric, default=90)
    canary_period = Column(Integer, default=2)
    band_count = Column(Integer, default=5)
    signals = relationship("canarypy.api.models.signal.Signal", backref="_release", lazy="dynamic")
    canary_bands = relationship("ReleaseCanaryBand", backref="_release", lazy="dynamic")

    @property
    def active_canary_band(self):
        return self.canary_bands.filter_by(is_active=True).first()


class ReleaseCanaryBand(Base):
    __tablename__ = "release_canary_band"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    release_id = Column(
        UUID(as_uuid=True), ForeignKey(f"release.id"), nullable=False
    )
    canary_executions = relationship("canarypy.api.models.signal.Signal", backref="_canary_band", lazy="dynamic")
    standard_executions = relationship("canarypy.api.models.signal.Signal", backref="_standard_band", lazy="dynamic")

    @property
    def end_date(self):
        return self.start_date + datetime.timedelta(seconds=self.duration)

    @property
    def is_active(self):
        return self.start_date <= func.now() <= self.end_date

    @property
    def duration(self):
        return (self.release.canary_period / self.release.band_count) * 24 * 60 * 60

    start_date = Column(DateTime, default=func.now())
    release = relationship("canarypy.api.models.release.Release")
