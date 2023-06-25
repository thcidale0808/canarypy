import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from canarypy.api.schemas.product import Product


class ReleaseCreate(BaseModel):
    id: Optional[UUID]
    artifact_url: str
    semver_version: str
    is_canary: Optional[bool] = True
    is_active: Optional[bool] = True
    threshold: Optional[float] = 80.0
    canary_period: Optional[float] = 2.0
    band_count: Optional[int]
    release_date: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class Release(BaseModel):
    id: Optional[UUID]
    semver_version: str
    product: Product

    class Config:
        orm_mode = True


class ReleaseCreateID(BaseModel):
    id: Optional[UUID]

    class Config:
        orm_mode = True
