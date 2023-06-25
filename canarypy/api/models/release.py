import datetime
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    and_,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import aliased, object_session, relationship
from sqlalchemy.sql import func

from canarypy.api.db.base import Base
from canarypy.api.models.signal import Signal


class Release(Base):
    __tablename__ = "release"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    product_id = Column(UUID(as_uuid=True), ForeignKey(f"product.id"), nullable=False)
    semver_version = Column(String(), nullable=True)
    product = relationship("canarypy.api.models.product.Product")
    release_date = Column(DateTime, default=datetime.datetime.now())
    is_canary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    threshold = Column(Numeric, default=90)
    canary_period = Column(Numeric, default=2.0)
    band_count = Column(Integer, default=5)
    signals = relationship(
        "canarypy.api.models.signal.Signal", backref="_release", lazy="dynamic"
    )
    canary_bands = relationship("ReleaseCanaryBand", backref="_release")

    @property
    def active_canary_band(self):
        return next((band for band in self.canary_bands if band.is_active), None)

    @property
    def active_canary_band_executed_pc(self):
        return self.active_canary_band.execution_pc

    @property
    def active_canary_band_pc(self):
        return self.active_canary_band.band_number / self.band_count * 100


class ReleaseCanaryBand(Base):
    __tablename__ = "release_canary_band"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    release_id = Column(UUID(as_uuid=True), ForeignKey(f"release.id"), nullable=False)

    @property
    def execution_pc(self):
        if self.canary_executions_count or self.standard_signal_count > 0:
            return (
                self.canary_executions_count
                / (self.canary_executions_count + self.standard_signal_count)
            ) * 100
        return 0

    @property
    def end_date(self):
        return self.start_date + datetime.timedelta(seconds=float(self.duration))

    @property
    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now <= self.end_date

    @property
    def duration(self):
        return (self.release.canary_period / self.release.band_count) * 24 * 60 * 60

    start_date = Column(DateTime, default=datetime.datetime.now())
    band_number = Column(Integer, default=1)
    release = relationship("canarypy.api.models.release.Release")

    @hybrid_property
    def canary_executions_count(self):
        return len(
            [
                signal
                for signal in self.signals
                if signal.is_canary and signal.release.is_active
            ]
        )

    @canary_executions_count.expression
    def canary_executions_count(cls):
        ReleaseAlias = aliased(Release)
        return (
            select([func.count(Signal.id)])
            .where(
                and_(
                    Signal.release_id == ReleaseAlias.id,
                    ReleaseAlias.is_canary == True,
                    ReleaseAlias.is_active == True,
                    Signal.release_canary_band_id == cls.id,
                    Signal.is_canary == True,
                )
            )
            .label("canary_executions_count")
        )

    @hybrid_property
    def standard_signal_count(self):
        return len(
            [
                signal
                for signal in self.signals
                if signal.is_canary is False and signal.release.is_active
            ]
        )

    @standard_signal_count.expression
    def standard_signal_count(cls):
        ReleaseAlias = aliased(Release)
        return (
            select([func.count(Signal.id)])
            .where(
                and_(
                    ReleaseAlias.is_canary == False,
                    ReleaseAlias.is_active == True,
                    Signal.release_canary_band_id == cls.id,
                    Signal.is_canary == False,
                )
            )
            .label("standard_signal_count")
        )

    signals = relationship(
        "canarypy.api.models.signal.Signal",
        backref="_release_canary_band",
        lazy="dynamic",
    )
