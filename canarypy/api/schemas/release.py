from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional
from canarypy.api.schemas.product import Product


class ReleaseCreate(BaseModel):
    id: Optional[UUID]
    artifact_url: str
    semver_version: str
    is_canary: bool
    is_active: bool
    threshold: float
    canary_period: float

    class Config:
        orm_mode = True


class Release(BaseModel):
    id: Optional[UUID]
    semver_version: str
    product: Product

    class Config:
        orm_mode = True