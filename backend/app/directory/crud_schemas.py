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
# Activity
#


class ActivityCreate(Base):
    path: LtreeField = Field(min_length=1)
    name: str | None = None


class ActivityUpdate(Base):
    dest_path: LtreeField | None = Field(default=None, min_length=1)
    name: str | None = None


class ActivityPublic(Base):
    id: uuid.UUID
    path: LtreeField
    name: str


#
# Org
#


class OrgPublic(Base):
    id: uuid.UUID
    name: str
    activities: list[ActivityPublic]
    members: list[PersonPublic] | None = None
    description: str | None = None
    contact: ContactPublic | None = None


class OrgCreate(Base):
    name: str
    activities: list[ActivityCreate] | None = None
    members: list[PersonCreate] | None = None
    description: str | None = None
    contact: ContactCreate | None = None


class OrgUpdate(Base):
    name: str | None = None
    activities: list[ActivityUpdate] | None = None
    members: list[PersonUpdate] | None = None
    description: str | None = None
    contact: ContactUpdate | None = None


#
# Person
#


class PersonPublic(Base):
    id: uuid.UUID
    firstname: str
    lastname: str


class PersonCreate(Base):
    firstname: str
    lastname: str


class PersonUpdate(Base):
    firstname: str | None = None
    lastname: str | None = None


#
# Contact
#


class ContactPublic(Base):
    email_address: EmailStr | None = None
    phone_number: str | None = None
    website: HttpUrl | None = None
    address: AddressGeoCreate | None = None


class ContactCreate(ContactPublic):
    pass


class ContactUpdate(ContactPublic):
    pass


#
# Address
#


class AddressGeoPublic(Base):
    q: str | None = None
    street: str | None = None
    postal_code: str | None = None
    city: str | None = None
    country: str | None = None
    geo_point: str | None = None


class AddressGeoCreate(AddressGeoPublic):
    pass


class AddressGeoUpdate(AddressGeoPublic):
    pass
