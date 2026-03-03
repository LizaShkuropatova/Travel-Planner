from typing import List
from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from database.models import Place
from schemas.place import PlaceCreate, PlaceUpdate
from services.projects import get_project, recalc_project_completed
from services.third_party_intg import artworks

MAX_PLACES_FOR_PROJECT = 10


def list_places(db: Session, project_id: int) -> List[Place]:
    get_project(db, project_id)

    stmt = select(Place).where(Place.project_id == project_id).order_by(Place.id)
    return db.execute(stmt).scalars().all()


def get_place(db: Session, project_id: int, place_id: int) -> Place:
    get_project(db, project_id)

    stmt = select(Place).where(Place.project_id == project_id, Place.id == place_id)
    place = db.execute(stmt).scalar_one_or_none()
    if place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place


def add_place(db: Session, project_id: int, payload: PlaceCreate) -> Place:
    get_project(db, project_id)

    # max 10 places in project
    count_stmt = select(func.count()).select_from(Place).where(Place.project_id == project_id)
    count = db.execute(count_stmt).scalar_one()
    if count >= MAX_PLACES_FOR_PROJECT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project cannot contain more than {MAX_PLACES_FOR_PROJECT} places",
        )

    if not artworks(payload.external_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External place not found in Art Institute API",
        )

    place = Place(
        project_id=project_id,
        external_id=payload.external_id,
        notes=payload.notes,
        visited=False,
    )
    db.add(place)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This external place is already added to the project",
        )

    db.refresh(place)
    return place


def update_place(db: Session, project_id: int, place_id: int, payload: PlaceUpdate) -> Place:
    place = get_place(db, project_id, place_id)

    data = payload.model_dump(exclude_unset=True)
    visited_changed = "visited" in data

    for key, value in data.items():
        setattr(place, key, value)

    db.commit()
    db.refresh(place)

    if visited_changed:
        recalc_project_completed(db, project_id)

    return place