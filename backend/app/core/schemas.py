from __future__ import annotations

import uuid
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from datetime import datetime
from typing import Annotated, Any, Generic, Literal, TypeVar

import geoalchemy2
import geojson_pydantic
from fastapi import Depends
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    WrapValidator,
    field_validator,
)

from app.activities.schemas import TreePublic
from app.core.db.models import (
    EventActorAssoc,
    OrgActorAssoc,
    TourActorAssoc,
)

T = TypeVar("T")


class PageParams(BaseModel):
    """Request query params for paginated API."""

    q: str | None = Field(default=None)
    limit: int = Field(default=10, gt=0, le=100)
    offset: int = Field(default=0, ge=0)


class ErrorResponse(BaseModel):
    detail: str


PageParamsDep = Annotated[PageParams, Depends()]


class PagedResponse(BaseModel, Generic[T]):
    """Response schema for any paged read request."""

    total: int
    limit: int
    offset: int
    results: list[T]


class OwnerPublic(BaseModel):
    id: uuid.UUID
    email: str
    person: OwnerPersonPublic | None = None


class OwnerPersonPublic(BaseModel):
    id: uuid.UUID
    name: str


class GroupOwnerPublic(BaseModel):
    id: uuid.UUID
    name: str


class PermissionMixin(BaseModel):
    owner_id: uuid.UUID | None = None
    owner: OwnerPublic | None = None

    group_owner_id: uuid.UUID | None = None
    group_owner: GroupOwnerPublic | None = None

    other_read: bool
    member_read: bool
    group_read: bool


def remove_uncomplete_assocs(
    assocs: Sequence[OrgActorAssoc | TourActorAssoc | EventActorAssoc],
) -> Sequence[OrgActorAssoc | TourActorAssoc | EventActorAssoc]:
    new_assocs = []
    for assoc in assocs:
        if isinstance(assoc, OrgActorAssoc):
            if assoc.org is not None and assoc.actor is not None:
                new_assocs.append(assoc)
        elif isinstance(assoc, TourActorAssoc):
            if assoc.tour is not None and assoc.actor is not None:
                new_assocs.append(assoc)  # type: ignore
        elif isinstance(assoc, EventActorAssoc):
            if assoc.event is not None and assoc.actor is not None:
                new_assocs.append(assoc)  # type: ignore
        else:
            raise ValueError("Unknown assoc type")

    return new_assocs


def is_recursion_validation_error(exc: ValidationError) -> bool:
    errors = exc.errors()
    return len(errors) == 1 and errors[0]["type"] == "recursion_loop"


@contextmanager
def suppress_recursion_validation_error() -> Iterator[None]:
    try:
        yield
    except ValidationError as exc:
        if not is_recursion_validation_error(exc):
            raise exc


def drop_cyclic_references(children, h):
    try:
        return h(children)
    except ValidationError as exc:
        if not (is_recursion_validation_error(exc) and isinstance(children, list)):
            raise exc

        value_without_cyclic_refs = []
        for child in children:
            with suppress_recursion_validation_error():
                value_without_cyclic_refs.extend(h([child]))
        return h(value_without_cyclic_refs)


class Base(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class ContactPublic(Base):
    email_address: str | None = None
    phone_number: str | None = None
    address: AddressPublic | None = None
    website: str | None = None


class AddressPublic(Base):
    q: str
    geom_point: geojson_pydantic.Point | None = None

    @field_validator("geom_point", mode="before")
    def serialize_geom_point(
        cls,
        v: geoalchemy2.WKBElement,
    ) -> geojson_pydantic.Point | None:
        """Plain serializer for GeomPoint"""
        if not v:
            return None

        if not isinstance(v, geoalchemy2.WKBElement):
            raise ValueError("Not a WKBElement")

        shape = geoalchemy2.shape.to_shape(v)

        coords = geojson_pydantic.types.Position2D(
            longitude=shape.coords[0][0], latitude=shape.coords[0][1]
        )
        return geojson_pydantic.Point(type="Point", coordinates=coords)


class ActorPublicBase(Base):
    id: uuid.UUID
    name: str
    contact: ContactPublic | None = None

    membership_assocs: Annotated[
        list[OrgAssocPublic],
        WrapValidator(drop_cyclic_references),
        BeforeValidator(remove_uncomplete_assocs),
    ]

    tour_assocs: Annotated[
        list[TourAssocPublic],
        WrapValidator(drop_cyclic_references),
        BeforeValidator(remove_uncomplete_assocs),
    ]


class OrgPublic(ActorPublicBase, PermissionMixin):
    type: Literal["Org"]
    description: str | None = None
    activities: list[TreePublic]

    member_assocs: Annotated[
        list[ActorAssocPublic],
        WrapValidator(drop_cyclic_references),
        BeforeValidator(remove_uncomplete_assocs),
    ]


class PersonPublic(ActorPublicBase, PermissionMixin):
    type: Literal["Person"]
    role: str | None = None


class EventPublic(Base, PermissionMixin):
    """
    Used for the /tours/{id} endpoint
    """

    description: str | None = None
    start_dt: datetime
    end_dt: datetime | None = None
    actor_assocs: Annotated[
        list[ActorAssocPublic],
        WrapValidator(drop_cyclic_references),
        BeforeValidator(remove_uncomplete_assocs),
    ] = []


class TourPublic(Base, PermissionMixin):
    """
    Used for the /tours endpoint
    """

    id: uuid.UUID
    name: str
    description: str | None = None
    year: int | None = None
    disciplines: list[TreePublic]
    mobilities: list[TreePublic]
    actor_assocs: Annotated[
        list[ActorAssocPublic],
        WrapValidator(drop_cyclic_references),
        BeforeValidator(remove_uncomplete_assocs),
    ] = []
    events: list[EventPublic]

    geojson: geojson_pydantic.FeatureCollection | None = None


class OrgAssocPublic(Base):
    org: OrgPublic
    data: dict[str, Any] | None = None


class TourAssocPublic(Base):
    tour: TourPublic
    data: dict[str, Any] | None = None


class EventAssocPublic(Base):
    event: EventPublic
    data: dict[str, Any] | None = None


class ActorAssocPublic(Base):
    actor: OrgPublic | PersonPublic = Field(discriminator="type")
    data: dict[str, Any] | None = None
