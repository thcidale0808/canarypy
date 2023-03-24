from pydantic import BaseModel, Field, Json
from uuid import UUID
from typing import Optional


class Product(BaseModel):
    id: Optional[UUID]
    description: str
    repository_url: str
    artifact_url: str

    class Config:
        orm_mode = True
