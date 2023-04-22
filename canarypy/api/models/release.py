from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from canarypy.api.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
