from sqlalchemy import (
    Column,
    String,

)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from canarypy.api.db.base import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    description = Column(String())
    repository_url = Column(String())
    artifact_url = Column(String())
    release = relationship("canarypy.api.models.release.Release")
