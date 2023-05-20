from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, Json


class Signal(BaseModel):
    id: Optional[UUID]
    artifact_url: str
    semver_version: str
    instance_id: str
    description: str
    status: str

    class Config:
        orm_mode = True
