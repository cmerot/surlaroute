from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import geoalchemy2
import shapely
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
)


class Base(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class PermissionMixin:
    other_read: bool | None = None
    group_read: bool | None = None
    member_read: bool | None = None


class TreeImport(Base):
    id: uuid.UUID | None = None
    path: str
    name: str | None = None


class ActorAssocImport(Base):
    actor: PersonImport | OrgImport
    data: dict[str, Any] | None = None


class TourAssocImport(Base):
    tour: TourImport
    data: dict[str, Any]


class OrgAssocImport(Base):
    org: OrgImport
    data: dict[str, Any] | None = None


class ContactImport(Base):
    id: uuid.UUID | None = None
    email_address: EmailStr | None = None
    phone_number: str | None = None
    website: HttpUrl | None = None
    address: AddressGeoImport | None = None

    @field_serializer("website")
    def serialize_http_url(v):
        return str(v)


class OrgImport(Base, PermissionMixin):
    id: uuid.UUID | None = None
    name: str
    description: str | None = None
    activities: list[TreeImport] | None = None
    member_assocs: list[ActorAssocImport] | None = None
    tour_assocs: list[TourAssocImport] | None = None
    contact: ContactImport | None = None
    type: str = "Org"


class PersonImport(Base, PermissionMixin):
    id: uuid.UUID | None = None
    name: str
    role: str | None = None
    contact: ContactImport | None = None
    type: str = "Person"
    membership_assocs: list[OrgAssocImport] | None = None
    user: UserImport | None = None


class AddressGeoImport(Base):
    q: str | None = None
    street: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None
    geom_point: geoalchemy2.WKBElement | None = None

    @field_validator("geom_point", mode="before")
    def validate_geom_point(v: str | None = None) -> geoalchemy2.WKBElement | None:  # type: ignore
        if not v:
            return None

        if not isinstance(v, str):
            raise ValueError("Not a string")

        try:
            lat, lon = map(float, v.split(",", 1))
            v = shapely.geometry.Point((lat, lon))  # type: ignore[assignment]
        except ValueError:
            raise ValueError(
                "geom_point must be a string in the format 'lat, lon' eg: '1.1, 2.2'"
            )

        shape = shapely.geometry.shape(v)  # type: ignore[arg-type]
        wkbelement = geoalchemy2.shape.from_shape(shape)
        return wkbelement


class EventImport(Base, PermissionMixin):
    id: uuid.UUID | None = None
    description: str | None = None
    start_dt: datetime | None = None
    end_dt: datetime | None = None
    # event_venue: OrgImport
    tour: TourImport
    actor_assocs: list[ActorAssocImport] | None = None

    @field_validator("start_dt", "end_dt", mode="before")
    def parse_datetime(cls, value):
        if isinstance(value, str):
            try:
                # Parse the string to a datetime object
                return datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                raise ValueError(
                    f"Invalid datetime format: {value}. Expected format: DD-MM-YYYY HH:MM:SS"
                )
        return value


class TourImport(Base, PermissionMixin):
    id: uuid.UUID | None = None
    name: str
    description: str | None = None
    events: list[EventImport] | None = None
    disciplines: list[TreeImport] | None = None
    mobilities: list[TreeImport] | None = None
    actor_assocs: list[ActorAssocImport] | None = None


class UserImport(Base):
    id: uuid.UUID | None = None
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_member: bool = False
    person: PersonImport | None = None
