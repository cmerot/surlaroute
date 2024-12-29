from __future__ import annotations

import uuid
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.schemas import (
    ContactPublic,
    PermissionMixin,
    TreePublic,
)


class Base(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        exclude_none=True,
        exclude_unset=True,
    )


class ActorBase_Explore(Base):
    id: uuid.UUID
    name: str
    contact: ContactPublic | None = None


class AssocBase_Explore(Base):
    data: dict[str, Any] | None = None


##
## LIGHT


class OrgLite_Explore(ActorBase_Explore):
    type: Literal["Org"]
    description: str | None = None
    activities: list[TreePublic]


class PersonLite_Explore(ActorBase_Explore):
    type: Literal["Person"]
    role: str | None = None


##
## BASE


class ActorLiteAssoc_Explore(AssocBase_Explore):
    type: Literal["actor"] = "actor"
    actor: OrgLite_Explore | PersonLite_Explore = Field(discriminator="type")


class OrgLiteAssoc_Explore(AssocBase_Explore):
    type: Literal["org"] = "org"
    org: OrgLite_Explore


class Org_Explore(OrgLite_Explore, PermissionMixin):
    pyd_org: str = "Org_Explore"
    membership_assocs: list[OrgLiteAssoc_Explore]
    member_assocs: list[ActorLiteAssoc_Explore]
    activities: list[TreePublic]


class Person_Explore(PersonLite_Explore, PermissionMixin):
    pyd_person: str = "Person_Explore"
    membership_assocs: list[OrgLiteAssoc_Explore]


##
## FULL


class ActorAssoc_Explore(ActorLiteAssoc_Explore):
    actor: Org_Explore | Person_Explore | None = Field(
        discriminator="type", default=None
    )


class OrgAssoc_Explore(OrgLiteAssoc_Explore):
    org: Org_Explore


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


class TourActorAssoc(Base):
    tour: TourLitePublic


class OrgFull_Explore(Org_Explore):
    pyd_org: str = "OrgFull_Explore"
    membership_assocs: list[OrgAssoc_Explore]
    member_assocs: list[ActorAssoc_Explore]
    tour_assocs: list[TourActorAssoc]


class PersonFull_Explore(Person_Explore):
    pyd_person: str = "PersonFull_Explore"

    @field_validator("membership_assocs", mode="before")
    def validate_assocs(v):
        return v

    membership_assocs: list[OrgAssoc_Explore]
