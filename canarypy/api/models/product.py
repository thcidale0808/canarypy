import uuid

from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from canarypy.api.db.base import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name = Column(String(), unique=True)
    repository_url = Column(String())
    artifact_url = Column(String())
    release = relationship("canarypy.api.models.release.Release")

    __table_args__ = (Index("idx_product_name", "name", unique=True),)
