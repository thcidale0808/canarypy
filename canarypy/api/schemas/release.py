from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional


class ReleaseCreate(BaseModel):
    id: Optional[UUID]
    artifact_url: str
    semver_version: str

    class Config:
        orm_mode = True


class Release(BaseModel):
    id: Optional[UUID]
    semver_version: str

    class Config:
        orm_mode = True