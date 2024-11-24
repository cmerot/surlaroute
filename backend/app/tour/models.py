from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

import app.directory.models
from app.core.db.base_class import Base


@dataclass
class Tour(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    # actor_assocs: Mapped[list[AssociationTourActor]] = relationship(
    #     cascade="all, delete-orphan",
    # )
    events: Mapped[list[Event]] = relationship(back_populates="tour")


@dataclass
class AssociationTourActor(Base):
    tour_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tour.id"),
        primary_key=True,
    )
    # tour: Mapped[Tour] = relationship(
    #     back_populates="actor_assocs",
    #     foreign_keys=[tour_id],
    # )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    # actor: Mapped[app.directory.models.Actor] = relationship(
    #     back_populates="tour_assocs",
    #     foreign_keys=[actor_id],
    # )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)


@dataclass
class Event(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    tour_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tour.id"))
    tour: Mapped[Tour] = relationship(back_populates="events")
    actor_assocs: Mapped[list[AssociationEventActor]] = relationship(
        cascade="all, delete-orphan",
    )
    start_dt: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    end_dt: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    event_venue_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("org.id"),
        default=None,
    )
    event_venue: Mapped[app.directory.models.Org] = relationship()


@dataclass
class AssociationEventActor(Base):
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event.id"),
        primary_key=True,
    )
    # event: Mapped[Event] = relationship(
    #     back_populates="actor_assocs",
    #     foreign_keys=[event_id],
    # )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    # actor: Mapped[app.directory.models.Actor] = relationship(
    #     back_populates="event_assocs",
    #     foreign_keys=[actor_id],
    # )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
