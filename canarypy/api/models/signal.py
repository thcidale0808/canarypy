from sqlalchemy import (
    Column,
    Boolean,
    ForeignKey,
    String
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from canarypy.api.db.base import Base
from sqlalchemy.orm import relationship


class Signal(Base):
    __tablename__ = "signal"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    release_id = Column(
        UUID(as_uuid=True), ForeignKey(f"release.id"), nullable=False
    )
    instance_id = Column(String(), nullable=False)
    description = Column(String(), nullable=True)
    status = Column(Boolean(), nullable=False)
    release = relationship("canarypy.api.models.release.Release")
