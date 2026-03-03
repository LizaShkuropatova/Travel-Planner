from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ProjectListOut
from services import projects as projects_service
from services import places as places_service

router = APIRouter()


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    if not payload.places or len(payload.places) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project must contain at least 1 place",
        )

    project = projects_service.create_project(db, payload)

    for place_payload in payload.places:
        places_service.add_place(db, project.id, place_payload)

    projects_service.recalc_project_completed(db, project.id)
    project = projects_service.get_project(db, project.id)
    return project


@router.get("", response_model=List[ProjectListOut])
def list_projects(db: Session = Depends(get_db)):
    return projects_service.list_projects(db)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return projects_service.get_project(db, project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    return projects_service.update_project(db, project_id, payload)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    projects_service.delete_project(db, project_id)
    return None