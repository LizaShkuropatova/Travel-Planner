from datetime import date
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    places: Mapped[List["Place"]] = relationship(
        "Place",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Place.id",
    )

class Place(Base):
    __tablename__ = "places"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_place_project_external"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    external_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    visited: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    project: Mapped["Project"] = relationship("Project", back_populates="places")
