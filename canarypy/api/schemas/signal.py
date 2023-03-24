from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional


class Signal(BaseModel):
    id: Optional[UUID]
    artifact_url: str
    semver_version: str
    instance_id: str
    description: str
    status: str

    class Config:
        orm_mode = True
