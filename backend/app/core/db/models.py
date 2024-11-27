from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Any

import unidecode
from geoalchemy2 import Geometry
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    foreign,
    mapped_column,
    relationship,
    remote,
)
from sqlalchemy_utils import Ltree, LtreeType


def is_pydantic(obj: object) -> bool:
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"


class Base(DeclarativeBase):
    __name__: str  # type: ignore
    # registry = default_registry

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def from_dto(cls, dto: BaseModel) -> Base:
        """
        see: https://stackoverflow.com/questions/64414030/how-to-use-nested-pydantic-models-for-sqlalchemy-in-a-flexible-way/76133080#76133080
        """
        obj = cls()
        properties = dict(dto)
        for key, value in properties.items():
            try:
                if is_pydantic(value):
                    value = getattr(cls, key).property.mapper.class_.from_dto(value)
                setattr(obj, key, value)
            except AttributeError as e:
                raise AttributeError(e)
        return obj


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str | None] = mapped_column(default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_member: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column()

    # There is a dependency person -> user for the ownership
    # This is another one to link a user to its very own Person.
    # To avoid cycling dep, we need to tell SA how to generate the schema
    # with use_alter
    # see https://docs.sqlalchemy.org/en/20/core/constraints.html#use-alter
    person_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("person.id", use_alter=True)
    )
    person: Mapped[Person | None] = relationship(
        foreign_keys=[person_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Permissions:
    """
    Mixin for permissions applied at least to Person, Org, Tour and Event.
    It must be declared first, eg `class Person(Permission, Actor)`
    because it will extract and autofill its own keys, then call the
    parent constructor.

    The owner is a User and the owner group is an Org.

    It defines read and write perms for:
    - the group
    - members
    - other (read only)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if "owner" in kwargs:
            pass
        super().__init__(*args, **kwargs)

    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("user.id"), default=None
    )

    @declared_attr
    def owner(self) -> Mapped[User]:
        return relationship(foreign_keys=[self.owner_id])  # type: ignore[list-item]

    group_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("org.id"), default=None
    )

    @declared_attr
    def group_owner(self) -> Mapped[Org]:
        return relationship(foreign_keys=[self.group_owner_id])  # type: ignore[list-item]

    group_read: Mapped[bool] = mapped_column(default=True)
    group_write: Mapped[bool] = mapped_column(default=True)
    member_read: Mapped[bool] = mapped_column(default=True)
    member_write: Mapped[bool] = mapped_column(default=False)
    other_read: Mapped[bool] = mapped_column(default=False)


class Actor(Base):
    """
    Base class for Person and Org, so each time we need to link either a
    Person or an Org we can use an Actor.

    The pattern is a *Joined Table Inheritance*.

    See https://docs.sqlalchemy.org/en/20/orm/inheritance.html#joined-table-inheritance
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column()

    """
    Store the memberships of an actor, ie which Org it belongs to.
    """
    membership_assocs: Mapped[list[AssociationOrgActor]] = relationship(
        # note: raises ValueError with back_populates="org"
        # ValueError: Bidirectional attribute conflict detected:
        # Passing object <Person at 0x7f89b57d4eb0> to attribute "AssociationOrgActor.actor"
        # triggers a modify event on attribute "AssociationOrgActor.org"
        # via the backref "Actor.memberships".
        # back_populates="org",
        cascade="all, delete-orphan",
    )
    event_assocs: Mapped[list[AssociationEventActor]] = relationship(
        cascade="all, delete-orphan",
    )
    tour_assocs: Mapped[list[AssociationTourActor]] = relationship(
        cascade="all, delete-orphan",
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("contact.id"),
        default=None,
    )
    contact: Mapped[Contact] = relationship()

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        if cls.__name__ == "Actor":
            return {
                "polymorphic_on": cls.type,
                "polymorphic_identity": cls.__name__,
                "confirm_deleted_rows": False,
            }
        else:
            return {
                "polymorphic_identity": cls.__name__,
            }


class Org(Permissions, Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column()
    activities: Mapped[list[Activity]] = relationship(
        secondary="associationorgactivity",
        back_populates="orgs",
    )
    member_assocs: Mapped[list[AssociationOrgActor]] = relationship(
        back_populates="org",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Person(Permissions, Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    firstname: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()


class AssociationOrgActivity(Base):
    """
    Activities of an org is a many-to-many relationship.

    See https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    """

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("org.id"), primary_key=True)
    activity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activity.id"), primary_key=True
    )


class AssociationOrgActor(Base):
    """
    Members of an org, it a many-to-many relationship with an Association Object,
    ie. we need to attach data to the relationship, so members won't be accessible
    directly, but will have the `member_assocs` and `membership_assocs` from
    where we can reach the `data` and the org or the actor.
    """

    org_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("org.id"),
        primary_key=True,
    )
    org: Mapped[Org] = relationship(
        back_populates="member_assocs",
        foreign_keys=[org_id],
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    actor: Mapped[Actor] = relationship(
        back_populates="membership_assocs",
        foreign_keys=[actor_id],
    )
    data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)

    def __repr__(self) -> str:
        return f"AssociationOrgActor({self.actor} in {self.org})"


class Activity(Base):
    """
    Activity represent what does an Org. They are hierarchical and implemented
    with Postgres LTree. The name attribute of an activity is closely tied to
    its path.
    LTree support comes from the `sqlalchemy_utils` package.
    """

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    path: Mapped[Ltree] = mapped_column(LtreeType, unique=True)
    name: Mapped[str] = mapped_column()
    schema: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    parent: Mapped[Activity] = relationship(
        "Activity",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        viewonly=True,
    )
    orgs: Mapped[list[Org]] = relationship(
        secondary="associationorgactivity",
        back_populates="activities",
    )

    def __init__(self, path: str | Ltree, **kwargs: Any) -> None:
        """
        Here we just wrap the path in a Ltree before forwarding init to the parent
        """
        super().__init__(**kwargs, path=Ltree(path))

    @staticmethod
    def slugify(s: str) -> str:
        s = unidecode.unidecode(s).lower().strip()
        s = re.sub(r"[^\w\s.-]", "", s)
        s = re.sub(r"[\s_-]+", "_", s)
        s = re.sub(r"^-+|-+$", "", s)
        s = re.sub(r"_+", "_", s)
        s = re.sub(r"\.(?=[\w_])", ".", s)
        return s


class Contact(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email_address: Mapped[str | None] = mapped_column(default=None)
    phone_number: Mapped[str | None] = mapped_column(default=None)
    website: Mapped[str | None] = mapped_column(default=None)
    address_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("addressgeo.id"),
        default=None,
    )
    address: Mapped[AddressGeo] = relationship()


class AddressGeo(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    street: Mapped[str | None] = mapped_column(default=None)
    postal_code: Mapped[str | None] = mapped_column(default=None)
    city: Mapped[str | None] = mapped_column(default=None)
    country: Mapped[str | None] = mapped_column(default=None)

    administrative_area_1: Mapped[str | None] = mapped_column(default=None)
    administrative_area_2: Mapped[str | None] = mapped_column(default=None)
    administrative_area_3: Mapped[str | None] = mapped_column(default=None)

    geo_location: Mapped[Geometry | None] = mapped_column(
        "geo_location",
        Geometry("POINT", srid=4326),
        default=None,
    )
    geo_shape: Mapped[Geometry | None] = mapped_column(
        "geo_shape",
        Geometry("POLYGON", srid=4326),
        default=None,
    )


class Tour(Base, Permissions):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    actor_assocs: Mapped[list[AssociationTourActor]] = relationship(
        cascade="all, delete-orphan",
    )
    events: Mapped[list[Event]] = relationship(back_populates="tour")


class Event(Base, Permissions):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
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
    event_venue: Mapped[Org] = relationship(foreign_keys=event_venue_id)


class AssociationTourActor(Base):
    tour_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tour.id"),
        primary_key=True,
    )
    tour: Mapped[Tour] = relationship(
        back_populates="actor_assocs",
        foreign_keys=[tour_id],
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    actor: Mapped[Actor] = relationship(
        back_populates="tour_assocs",
        foreign_keys=[actor_id],
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)


class AssociationEventActor(Base):
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("event.id"),
        primary_key=True,
    )
    event: Mapped[Event] = relationship(
        back_populates="actor_assocs",
        foreign_keys=[event_id],
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    actor: Mapped[Actor] = relationship(
        back_populates="event_assocs",
        foreign_keys=[actor_id],
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
