from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional


class Release(BaseModel):
    id: Optional[UUID]
    product_id: UUID
    semver_version: str

    class Config:
        orm_mode = True
