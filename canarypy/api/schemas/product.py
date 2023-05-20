from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, Json


class Product(BaseModel):
    id: Optional[UUID]
    name: str
    repository_url: str
    artifact_url: str

    class Config:
        orm_mode = True
