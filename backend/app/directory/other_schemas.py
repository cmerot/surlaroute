from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict

from app.directory.crud_schemas import LtreeField


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


#
# Activity
#


class ActivityImport(Base):
    id: uuid.UUID | None = None
    path: LtreeField
    name: str | None = None
    is_selectable: bool | None = True


#
# Org
#


class OrgImport(Base):
    id: uuid.UUID | None = None
    name: str
    activities: list[ActivityImport] = []
    members: list[PersonImport] = []
    description: str | None = None
    contact: ContactImport | None = None


#
# User
#


class UserImport(Base):
    id: uuid.UUID | None = None
    password: str | None = None
    person: PersonImport | None = None


#
# Person
#


class PersonImport(Base):
    id: uuid.UUID | None = None
    firstname: str | None = None
    laststname: str | None = None
    contact: ContactImport | None = None


#
# Contact
#


class ContactImport(Base):
    id: uuid.UUID | None = None
    address: AddressImport | None = None


#
# Address
#


class AddressImport(Base):
    id: uuid.UUID | None = None
