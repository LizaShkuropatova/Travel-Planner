from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.place import PlaceCreate, PlaceOut, PlaceUpdate
from services import places as places_service

router = APIRouter()


@router.post("/{project_id}/places", response_model=PlaceOut, status_code=status.HTTP_201_CREATED)
def add_place(project_id: int, payload: PlaceCreate, db: Session = Depends(get_db)):
    return places_service.add_place(db, project_id, payload)


@router.get("/{project_id}/places", response_model=List[PlaceOut])
def list_places(project_id: int, db: Session = Depends(get_db)):
    return places_service.list_places(db, project_id)


@router.get("/{project_id}/places/{place_id}", response_model=PlaceOut)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    return places_service.get_place(db, project_id, place_id)


@router.patch("/{project_id}/places/{place_id}", response_model=PlaceOut)
def update_place(project_id: int, place_id: int, payload: PlaceUpdate, db: Session = Depends(get_db)):
    return places_service.update_place(db, project_id, place_id, payload)