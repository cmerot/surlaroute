from __future__ import annotations

import uuid
from typing import Annotated

import unidecode
from pydantic import (
    BaseModel,
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
    model_config = ConfigDict(from_attributes=True)


LtreeField = Annotated[
    str | Ltree,
    PlainValidator(
        lambda o: o if isinstance(o, Ltree) else Ltree(unidecode.unidecode(o))
    ),
    PlainSerializer(lambda o: o.path, return_type=str),
    WithJsonSchema({"type": "string", "examples": ["some.path"]}),
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
    actor: PersonPublic | OrgPublic | None = None


class ActorAssocCreate(Base):
    actor: PersonCreate | OrgCreate | None = None


class ActorAssocUpdate(Base):
    actor: PersonUpdate | OrgUpdate | None = None


class ActorAssocImport(Base):
    actor: PersonImport | OrgImport | None = None


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
    contact: ContactImport | None = None
    type_: str | None = None


# Person


class PersonBase(Base):
    name: str
    role: str | None = None


class PersonPublic(PersonBase):
    id: uuid.UUID
    contact: ContactPublic | None = None


class PersonCreate(PersonBase):
    contact: ContactCreate | None = None


class PersonUpdate(PersonBase):
    contact: ContactUpdate | None = None


class PersonImport(PersonBase):
    id: uuid.UUID | None = None
    contact: ContactImport | None = None
    type_: str


# Contact


class ContactBase(Base):
    email_address: EmailStr | None = None
    phone_number: str | None = None
    website: HttpUrl | None = None


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
    # geo_location: str | None = None


class AddressGeoPublic(AddressGeoBase):
    id: uuid.UUID


class AddressGeoCreate(AddressGeoBase):
    pass


class AddressGeoUpdate(AddressGeoBase):
    pass


class AddressGeoImport(AddressGeoBase):
    pass


# Tour


class TourImport(Base):
    id: uuid.UUID | None = None
    name: str
    description: str | None = None
    events: list[EventImport] | None = None
    disciplines: list[TreeImport] | None = None
    mobilities: list[TreeImport] | None = None
    actor_assocs: list[ActorAssocImport] | None = None


# Event


class EventImport(Base):
    id: uuid.UUID | None = None
    description: str | None = None
    start_dt: str | None = None
    end_dt: str | None = None
    event_venue: OrgImport
    tour: TourImport
    actor_assocs: list[ActorAssocImport] | None = None
