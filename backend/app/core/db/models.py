from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Envelope, ST_Union
from sqlalchemy import (
    Column,
    ColumnElement,
    DateTime,
    ForeignKey,
    Select,
    and_,
    func,
    or_,
    select,
    true,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declared_attr,
    mapped_column,
    relationship,
)
from sqlalchemy.orm.session import ORMExecuteState
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy_utils import Ltree
from sqlalchemy_utils.types import LtreeType

#
# Bases, mixins and user
#


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class PermissionsMixin:
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

    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("user.id"), default=None
    )

    @declared_attr
    def owner(self) -> Mapped[User]:
        return relationship(foreign_keys=[self.owner_id])  # type: ignore[list-item]

    group_owner_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("org.id", use_alter=True), default=None
    )

    @declared_attr
    def group_owner(cls) -> Mapped[Org]:
        return relationship(foreign_keys=[cls.group_owner_id], remote_side="Org.id")  # type: ignore[list-item]

    group_read: Mapped[bool] = mapped_column(default=True)
    group_write: Mapped[bool] = mapped_column(default=True)
    member_read: Mapped[bool] = mapped_column(default=True)
    member_write: Mapped[bool] = mapped_column(default=False)
    other_read: Mapped[bool] = mapped_column(default=False)


class Base(DeclarativeBase):
    __name__: str  # type: ignore

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TreeBase(Base):
    """
    A hierarchical tree implemented with Postgres LTree.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    path: Mapped[Ltree] = mapped_column(LtreeType, unique=True)
    name: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "path":
            value = Ltree(value)
        super().__setattr__(name, value)


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
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
        back_populates="user",
    )

    _group_ids: list[uuid.UUID] = []

    @property
    def group_ids(self) -> list[uuid.UUID]:
        return self._group_ids

    def set_group_ids(self) -> None:
        if self.person:
            self._group_ids = [m.org_id for m in self.person.membership_assocs]

    def __repr__(self) -> str:
        if not self.email:
            return super().__repr__()
        return f"{self.__class__.__name__}(id={self.id} email={self.email})"


#
# Business classes
#


class Actor(PermissionsMixin, Base):
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
    membership_assocs: Mapped[list[OrgActorAssoc]] = relationship(
        # note: raises ValueError with back_populates="org"
        # ValueError: Bidirectional attribute conflict detected:
        # Passing object <Person at 0x7f89b57d4eb0> to attribute "AssociationOrgActor.actor"
        # triggers a modify event on attribute "AssociationOrgActor.org"
        # via the backref "Actor.memberships".
        # back_populates="org",
        cascade="all, delete-orphan",
    )
    event_assocs: Mapped[list[EventActorAssoc]] = relationship(
        cascade="all, delete-orphan",
    )
    tour_assocs: Mapped[list[TourActorAssoc]] = relationship(
        cascade="all, delete-orphan",
    )
    contact_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("contact.id"),
        default=None,
    )
    contact: Mapped[Contact] = relationship(back_populates="actor")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "Actor",
        "confirm_deleted_rows": False,
    }


class Org(Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(default=None)
    activities: Mapped[list[Activity]] = relationship(
        secondary="orgactivity",
        back_populates="orgs",
    )
    member_assocs: Mapped[list[OrgActorAssoc]] = relationship(
        back_populates="org",
        cascade="all, delete-orphan",
    )
    __mapper_args__ = {
        "polymorphic_identity": "Org",
        "inherit_condition": id == Actor.id,
    }

    def __repr__(self) -> str:
        if not self.name:
            return super().__repr__()
        return f"{self.__class__.__name__}(id={self.id} name={self.name})"


class Person(Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column()
    role: Mapped[str | None] = mapped_column(default=None)
    user: Mapped[User | None] = relationship(
        back_populates="person", foreign_keys=[User.person_id]
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id} other_read={self.other_read} owner_id={self.owner_id})"
        # if not self.name:
        #     return super().__repr__()

    __mapper_args__ = {
        "polymorphic_identity": "Person",
    }


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
    actor: Mapped[Actor] = relationship()


class AddressGeo(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    q: Mapped[str | None] = mapped_column(default=None)
    street: Mapped[str | None] = mapped_column(default=None)
    postal_code: Mapped[str | None] = mapped_column(default=None)
    city: Mapped[str | None] = mapped_column(default=None)
    country: Mapped[str | None] = mapped_column(default=None)

    administrative_area_1: Mapped[str | None] = mapped_column(default=None)
    administrative_area_2: Mapped[str | None] = mapped_column(default=None)
    administrative_area_3: Mapped[str | None] = mapped_column(default=None)

    geom_point: Mapped[Geometry | None] = mapped_column(Geometry("POINT", srid=4326))
    geom_shape: Mapped[Geometry | None] = mapped_column(Geometry("POLYGON", srid=4326))

    def __repr__(self) -> str:
        if not self.q:
            return super().__repr__()
        return f"{self.__class__.__name__}({self.q})"


class Tour(Base, PermissionsMixin):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(default=None)

    disciplines: Mapped[list[Discipline]] = relationship(
        secondary="tourdiscipline",
        back_populates="tours",
    )
    mobilities: Mapped[list[Mobility]] = relationship(
        secondary="tourmobility",
        back_populates="tours",
    )
    events: Mapped[list[Event]] = relationship(back_populates="tour")
    actor_assocs: Mapped[list[TourActorAssoc]] = relationship(
        cascade="all, delete-orphan",
    )

    @hybrid_property
    def year(self) -> int | None:
        if self.events:
            # Filter out None values and get the year
            years = [
                event.start_dt.year
                for event in self.events
                if event.start_dt is not None
            ]
            return min(years) if years else None
        return None

    @year.expression  # type: ignore[no-redef]
    def year(cls):
        return (
            select(func.extract("year", func.min(Event.start_dt)))
            .where(Event.tour_id == cls.id)
            .correlate(cls)
            .label("year")
        )

    @hybrid_property
    def producers(self) -> list[Actor]:
        if self.actor_assocs:
            return [
                a.actor
                for a in self.actor_assocs
                if a.data and a.data.get("role") == "producer"
            ]
        return []

    @producers.expression  # type: ignore[no-redef]
    def producers(cls):
        return (
            select(Actor)
            .join(TourActorAssoc, Actor.id == TourActorAssoc.actor_id)
            .join(Tour, Tour.id == TourActorAssoc.tour_id)
            .where(Tour.id == cls.id)
            .where(
                func.jsonb_extract_path_text(TourActorAssoc.data, "role") == "producer"
            )
            .subquery()
        )

    @hybrid_property
    def bbox(self):
        """Returns the bounding box of all address points associated with the tour"""
        raise NotImplementedError("Hybrid properties can't execute complex SQL")

    @bbox.expression  # type: ignore[no-redef]
    def bbox(cls):
        """SQL expression for calculating the tour's bounding box"""
        return (
            select(ST_Envelope(ST_Union(AddressGeo.geom_point)))
            .join(Contact, AddressGeo.id == Contact.address_id)
            .join(Actor, Contact.id == Actor.contact_id)
            .join(EventActorAssoc, Actor.id == EventActorAssoc.actor_id)
            .join(Event, EventActorAssoc.event_id == Event.id)
            .filter(Event.tour_id == cls.id)
            .scalar_subquery()
        )

    def __repr__(self) -> str:
        if not self.name:
            return super().__repr__()
        return f"{self.__class__.__name__}({self.name})"


class Event(Base, PermissionsMixin):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str | None] = mapped_column(default=None)
    description: Mapped[str | None] = mapped_column(default=None)
    start_dt: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
    end_dt: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )

    tour_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tour.id"))
    tour: Mapped[Tour] = relationship(back_populates="events")

    actor_assocs: Mapped[list[EventActorAssoc]] = relationship(
        cascade="all, delete-orphan",
    )

    @hybrid_property
    def event_venues(self) -> list[Actor]:
        if self.actor_assocs:
            return [
                a.actor
                for a in self.actor_assocs
                if a.data and a.data.get("role") == "diffusion"
            ]
        return []

    @event_venues.expression  # type: ignore[no-redef]
    def event_venues(cls):
        return (
            select(Actor)
            .join(EventActorAssoc, Actor.id == EventActorAssoc.actor_id)
            .join(Event, Event.id == EventActorAssoc.tour_id)
            .where(Event.id == cls.id)
            .where(
                func.jsonb_extract_path_text(EventActorAssoc.data, "role")
                == "diffusion"
            )
            .subquery()
        )


#
# Tags
#


class Activity(TreeBase):
    schema: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    orgs: Mapped[list[Org]] = relationship(
        secondary="orgactivity",
        back_populates="activities",
        # cascade="all, delete-orphan",
    )


class Discipline(TreeBase):
    tours: Mapped[list[Tour]] = relationship(
        secondary="tourdiscipline",
        back_populates="disciplines",
        # cascade="all, delete-orphan",
    )


class Mobility(TreeBase):
    tours: Mapped[list[Tour]] = relationship(
        secondary="tourmobility",
        back_populates="mobilities",
        # cascade="all, delete-orphan",
    )


#
# Many to many relation tables
#


class OrgActivity(Base):
    """
    Activities of an org is a many-to-many relationship.

    See https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    """

    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("org.id"), primary_key=True)
    activity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activity.id"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(org_id={self.org_id} activity_id={self.activity_id})"


class OrgActorAssoc(Base):
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
        return (
            f"{self.__class__.__name__}(org_id={self.org_id} actor_id={self.actor_id})"
        )


class TourActorAssoc(Base):
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tour_id={self.tour_id} actor_id={self.actor_id})"


class TourDiscipline(Base):
    tour_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tour.id"), primary_key=True)
    discipline_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("discipline.id"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tour_id={self.tour_id} discipline_id={self.discipline_id})"


class TourMobility(Base):
    tour_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tour.id"), primary_key=True)
    mobility_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("mobility.id"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tour_id={self.tour_id} mobility_id={self.mobility_id})"


class EventActorAssoc(Base):
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(event_id={self.event_id} actor_id={self.actor_id})"


#
#
#
def filter_out_actor_assocs(
    assocs: list[EventActorAssoc | TourActorAssoc | OrgActorAssoc],
) -> list[EventActorAssoc | TourActorAssoc | OrgActorAssoc]:
    def cleanActor(
        assoc: EventActorAssoc | TourActorAssoc | OrgActorAssoc,
    ) -> EventActorAssoc | TourActorAssoc | OrgActorAssoc:
        if isinstance(assoc.actor, Org):
            new_assocs = []
            for member_assoc in assoc.actor.member_assocs:
                if member_assoc.actor is not None:
                    new_assocs.append(member_assoc)
            assoc.actor.member_assocs = new_assocs
        return assoc

    new_assocs = []

    for assoc in assocs:
        if assoc.actor:
            if isinstance(assoc, EventActorAssoc) and assoc.event:
                new_assocs.append(cleanActor(assoc))
            elif isinstance(assoc, TourActorAssoc) and assoc.tour:
                new_assocs.append(cleanActor(assoc))
            elif isinstance(assoc, OrgActorAssoc) and assoc.org:
                new_assocs.append(cleanActor(assoc))
            else:
                pass
                # print("filtered out", assoc)
        else:
            pass
            # print("filtered out", assoc)

    return new_assocs


def get_model_from_table_name(table_name: str) -> type[Base] | None:
    for mapper in Base.registry.mappers:
        if mapper.class_.__tablename__ == table_name:
            return mapper.class_
    return None


def get_permission_filter(
    model: type[PermissionsMixin], user: User | None
) -> BooleanClauseList | ColumnElement[bool]:
    """
    Return a filter for the given model and user.
    """
    if user and user.is_superuser:
        return true()

    criteria = []

    # Public other_read gives access
    criteria.append(model.other_read == True)  # noqa: E712

    # If no user is logged in, that's it
    if not user:
        return or_(*criteria)

    # Ownership: a user can select its own entities
    if user.id:
        criteria.append(model.owner_id == user.id)

    # If the user is a member, the entity may be available
    if user.is_member:
        criteria.append(model.member_read == True)  # noqa: E712

    # If the user is a member of a group, the entity may be available
    criteria.append(
        and_(
            model.group_read == True,  # noqa: E712
            model.group_owner_id.in_(user.group_ids),
        )
    )

    return or_(*criteria)


@listens_for(Session, "do_orm_execute")
def add_permission_filters_on_select(orm_execute_state: ORMExecuteState) -> None:
    """
    On Session `do_orm_execute` event, add filters on subclasses of PermissionsMixin
    by inspecting the exported_columns of the statement.
    """

    if not isinstance(orm_execute_state.statement, Select):
        return

    user = orm_execute_state.session.info.get("user")

    models = set()

    # First pass to build the models set
    for col in orm_execute_state.statement.exported_columns:
        # Could have a func instead of a real col
        if not isinstance(col, Column):
            continue
        model = get_model_from_table_name(col.table.name)
        if model:
            models.add(model)

    # Second pass, add filters
    for model in models:
        if issubclass(model, PermissionsMixin) or isinstance(model, Actor):
            orm_execute_state.statement = orm_execute_state.statement.filter(
                get_permission_filter(model, user)
            )
