from typing import Optional
from pydantic import BaseModel, ConfigDict


class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceOut(BaseModel):
    id: int
    project_id: int
    external_id: str
    notes: Optional[str]
    visited: bool
    model_config = ConfigDict(from_attributes=True)