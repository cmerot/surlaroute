from __future__ import annotations

import json
import uuid
from datetime import datetime
from typing import Annotated, Any

import geoalchemy2
import geojson_pydantic
import geojson_pydantic.types
import shapely
import unidecode
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    HttpUrl,
    PlainSerializer,
    PlainValidator,
    WithJsonSchema,
)
from sqlalchemy_utils import Ltree


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


LtreeField = Annotated[
    str | Ltree,
    PlainValidator(
        lambda o: o if isinstance(o, Ltree) else Ltree(unidecode.unidecode(o))
    ),
    PlainSerializer(lambda o: o.path, return_type=str),
    WithJsonSchema({"type": "string", "examples": ["some.path"]}),
]

HttpUrlField = Annotated[
    str | HttpUrl,
    PlainSerializer(lambda o: str(o), return_type=str),
]

DatatimeField = Annotated[
    str | datetime,
    PlainValidator(
        lambda o: o if isinstance(o, datetime) else datetime.strptime(o, "%d/%m/%Y")
    ),
]


def validate_json(v: str | dict[str, Any]) -> str:
    if isinstance(v, str):
        return v
    return json.dumps(v)


JsonField = Annotated[
    str | dict[str, Any],
    PlainValidator(validate_json),
]


def validate_geom_point(
    v: str | shapely.geometry.base.BaseGeometry | geoalchemy2.WKBElement,
) -> geoalchemy2.WKBElement | None:
    if not v:
        return None

    if isinstance(v, geoalchemy2.WKBElement):
        return v

    if isinstance(v, str):
        try:
            lat, lon = map(float, v.split(",", 1))
            print(lat, lon)
            v = shapely.geometry.Point((lat, lon))
        except ValueError:
            raise ValueError(
                "geom_point must be a string in the format 'lat, lon' eg: '1.1, 2.2'"
            )

    shape = shapely.geometry.shape(v)
    wkbelement = geoalchemy2.shape.from_shape(shape)
    return wkbelement


def serialize_geom_point(
    v: geoalchemy2.WKBElement | geojson_pydantic.Point,
) -> geojson_pydantic.Point | None:
    if not v:
        return None

    if isinstance(v, geojson_pydantic.Point):
        return v

    shape = geoalchemy2.shape.to_shape(v)

    coords = geojson_pydantic.types.Position2D(
        latitude=shape.coords[0][0], longitude=shape.coords[0][1]
    )
    return geojson_pydantic.Point(type="Point", coordinates=coords)


GeomPoint = Annotated[
    str | geoalchemy2.WKBElement | geojson_pydantic.Point,
    BeforeValidator(validate_geom_point),
    PlainSerializer(serialize_geom_point, when_used="json"),
]


#
# Generic Tree and many to many
#

# Tree


class TreePublic(Base):
    id: uuid.UUID | None = None
    path: LtreeField
    name: str


class TreeCreate(Base):
    path: LtreeField = Field(min_length=1)
    name: str | None = None


class TreeUpdate(Base):
    dest_path: LtreeField | None = Field(default=None, min_length=1)
    name: str | None = None


class TreeImport(Base):
    id: uuid.UUID | None = None
    path: LtreeField
    name: str | None = None


# Many to many relation tables


class ActorAssocPublic(Base):
    """
    used to map any many-to-many relation impliying an actor
    ex: OrgActorAssoc requires an org and an actor, so to render
    the relation we'll use this. If we use a more specialized
    model with actor and org, there will be recursion:
    Org.member_assocs.org.member_assocs.org, ...

    """

    actor: PersonPublic | OrgPublic


class OrgAssocPublic(Base):
    """
    same than ActorAssocPublic but for from the POV of an actor
    """

    org: OrgPublic


class ActorAssocCreate(Base):
    actor: PersonCreate | OrgCreate | None = None


class ActorAssocUpdate(Base):
    actor: PersonUpdate | OrgUpdate | None = None


class ActorAssocImport(Base):
    actor: PersonImport | OrgImport
    data: JsonField | None = None


class TourAssocImport(Base):
    tour: TourImport
    data: JsonField | None = None


class OrgAssocImport(Base):
    org: OrgImport


#
# Business classes
#


# Org


class OrgBase(Base):
    description: str | None = None


class OrgPublic(OrgBase):
    id: uuid.UUID
    name: str
    activities: list[TreePublic] | None = None
    member_assocs: list[ActorAssocPublic] | None = None
    contact: ContactPublic | None = None


class OrgCreate(OrgBase):
    name: str
    activities: list[TreeCreate] | None = None
    member_assocs: list[ActorAssocCreate] | None = None
    contact: ContactCreate | None = None


class OrgUpdate(OrgBase):
    name: str | None = None
    activities: list[TreeUpdate] | None = None
    member_assocs: list[ActorAssocUpdate] | None = None
    contact: ContactUpdate | None = None


class OrgImport(OrgBase):
    id: uuid.UUID | None = None
    name: str
    activities: list[TreeImport] | None = None
    member_assocs: list[ActorAssocImport] | None = None
    tour_assocs: list[TourAssocImport] | None = None
    contact: ContactImport | None = None
    type_: str = "Org"


# Person


class PersonBase(Base):
    name: str
    role: str | None = None


class PersonPublic(PersonBase):
    id: uuid.UUID
    contact: ContactPublic | None = None
    membership_assocs: list[OrgAssocPublic] | None = None


class PersonCreate(PersonBase):
    contact: ContactCreate | None = None


class PersonUpdate(PersonBase):
    contact: ContactUpdate | None = None


class PersonImport(PersonBase):
    id: uuid.UUID | None = None
    contact: ContactImport | None = None
    type_: str = "Person"
    membership_assocs: list[OrgAssocImport] | None = None
    user: UserImport | None = None


# Contact


class ContactBase(Base):
    email_address: EmailStr | None = None
    phone_number: str | None = None
    website: HttpUrlField | None = None


class ContactPublic(ContactBase):
    id: uuid.UUID
    address: AddressGeoPublic | None = None


class ContactCreate(ContactBase):
    address: AddressGeoCreate | None = None


class ContactUpdate(ContactBase):
    address: AddressGeoUpdate | None = None


class ContactImport(ContactBase):
    id: uuid.UUID | None = None
    address: AddressGeoImport | None = None


# AddressGeo


class AddressGeoBase(Base):
    q: str | None = None
    street: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None
    geom_point: GeomPoint | None = None


class AddressGeoPublic(AddressGeoBase):
    id: uuid.UUID


class AddressGeoCreate(AddressGeoBase):
    pass


class AddressGeoUpdate(AddressGeoBase):
    pass


class AddressGeoImport(AddressGeoBase):
    pass


# Tour


class TourBase(Base):
    name: str
    description: str | None = None
    year: int | None = None


class TourPublic(TourBase):
    id: uuid.UUID
    events: list[EventPublic] | None = None
    disciplines: list[TreePublic] | None = None
    mobilities: list[TreePublic] | None = None
    actor_assocs: list[ActorAssocPublic] | None = None


class TourImport(TourBase):
    id: uuid.UUID | None = None
    events: list[EventImport] | None = None
    disciplines: list[TreeImport] | None = None
    mobilities: list[TreeImport] | None = None
    actor_assocs: list[ActorAssocImport] | None = None


# Event


class EventBase(Base):
    description: str | None = None
    start_dt: DatatimeField | None = None
    end_dt: DatatimeField | None = None


class EventPublic(EventBase):
    id: uuid.UUID
    event_venue: OrgPublic
    # Prevent recursion
    # tour: TourPublic
    actor_assocs: list[ActorAssocPublic] | None = None


class EventImport(EventBase):
    id: uuid.UUID | None = None
    event_venue: OrgImport
    tour: TourImport
    actor_assocs: list[ActorAssocImport] | None = None


# User


class UserImport(Base):
    id: uuid.UUID | None = None
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_member: bool = False
    person: PersonImport | None = None
