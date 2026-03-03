from typing import List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import Place, Project
from schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
        completed=False,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session) -> List[Project]:
    stmt = select(Project).order_by(Project.id)
    return db.execute(stmt).scalars().all()


def get_project(db: Session, project_id: int) -> Project:
    stmt = select(Project).where(Project.id == project_id)
    project = db.execute(stmt).scalar_one_or_none()
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


def update_project(db: Session, project_id: int, payload: ProjectUpdate) -> Project:
    project = get_project(db, project_id)

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project_id: int) -> None:
    project = get_project(db, project_id)
    visited_stmt = (
        select(Place.id)
        .where(Place.project_id == project_id, Place.visited.is_(True))
        .limit(1)
    )

    has_visited = db.execute(visited_stmt).first() is not None
    if has_visited:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project cannot be deleted because it has visited places",
        )

    db.delete(project)
    db.commit()


def recalc_project_completed(db: Session, project_id: int) -> Project:
    project = get_project(db, project_id)
    places_stmt = select(Place).where(Place.project_id == project_id)
    places = db.execute(places_stmt).scalars().all()
    project.completed = bool(places) and all(p.visited for p in places)
    db.commit()
    db.refresh(project)
    return project