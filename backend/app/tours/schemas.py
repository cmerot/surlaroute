from __future__ import annotations

import uuid
from datetime import datetime

from app.core.schemas import Base, TreePublic
from app.explore.schemas import ActorAssoc_Explore


class PermissionMixin:
    owner_id: uuid.UUID | None = None
    group_owner_id: uuid.UUID | None = None

    other_read: bool
    member_read: bool
    group_read: bool

    owner: OwnerPublic | None = None


class OwnerPersonPublic(Base):
    id: uuid.UUID
    name: str


class OwnerPublic(Base):
    person: OwnerPersonPublic | None = None


class TourLitePublic(Base, PermissionMixin):
    """
    Used for the /tours endpoint
    """

    id: uuid.UUID
    name: str
    description: str | None = None
    year: int | None = None
    disciplines: list[TreePublic]
    mobilities: list[TreePublic]


class EventLitePublic(Base, PermissionMixin):
    """
    Used for the /tours/{id} endpoint
    """

    description: str | None = None
    start_dt: datetime
    end_dt: datetime | None = None
    actor_assocs: list[ActorAssoc_Explore] = []


class TourPublic(Base, PermissionMixin):
    """
    Used for the /tours/{id} endpoint
    """

    id: uuid.UUID
    name: str
    description: str | None = None
    year: int | None = None
    events: list[EventLitePublic]
    disciplines: list[TreePublic]
    mobilities: list[TreePublic]
    actor_assocs: list[ActorAssoc_Explore] = []
