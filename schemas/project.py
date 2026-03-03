from datetime import date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from schemas.place import PlaceCreate, PlaceOut


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    completed: bool
    places: List[PlaceOut] = []
    model_config = ConfigDict(from_attributes=True)

class ProjectListOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    completed: bool

    model_config = ConfigDict(from_attributes=True)