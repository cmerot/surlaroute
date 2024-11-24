from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import unidecode
from geoalchemy2 import Geometry
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    Mapped,
    foreign,
    mapped_column,
    relationship,
    remote,
)
from sqlalchemy_utils import Ltree, LtreeType

from app.core.db.base_class import Base
from app.tour.models import AssociationEventActor, AssociationTourActor


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class PermissionsMixin:
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("org.id"), nullable=False)
    group_read: Mapped[bool] = mapped_column(default=True, nullable=False)
    group_write: Mapped[bool] = mapped_column(default=True, nullable=False)
    member_read: Mapped[bool] = mapped_column(default=True, nullable=False)
    member_write: Mapped[bool] = mapped_column(default=False, nullable=False)
    other_read: Mapped[bool] = mapped_column(default=False, nullable=False)


@dataclass
class AssociationOrgActivity(Base):
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("org.id"), primary_key=True)
    activity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("activity.id"), primary_key=True
    )


@dataclass
class AssociationOrgActor(Base):
    org_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("org.id"),
        primary_key=True,
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    actor: Mapped[Actor] = relationship(
        back_populates="membership_assocs",
        foreign_keys=[actor_id],
    )
    org: Mapped[Org] = relationship(
        back_populates="member_assocs",
        foreign_keys=[org_id],
    )
    data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)

    def __repr__(self) -> str:
        return f"AssociationOrgActor({self.actor} in {self.org})"


@dataclass
class Actor(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
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
            return {"polymorphic_identity": cls.__name__}

    def __str__(self) -> str:
        if self.__class__.__name__ == "Actor":
            return super().__str__()
        else:
            return f"{self.name}"  # type: ignore[attr-defined]

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        if "id" not in kwargs:
            kwargs["id"] = uuid.uuid4()
        super().__init__(**kwargs)


@dataclass
class Org(Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column()
    activities: Mapped[list[Activity]] = relationship(
        secondary=AssociationOrgActivity.__tablename__,
        back_populates="orgs",
    )
    member_assocs: Mapped[list[AssociationOrgActor]] = relationship(
        back_populates="org",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Person(Actor):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


@dataclass
class Activity(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    schema: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    label: Mapped[str | None] = mapped_column(default=None)
    path: Mapped[Ltree] = mapped_column(LtreeType, unique=True)
    parent: Mapped[Activity] = relationship(
        "Activity",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        viewonly=True,
    )
    orgs: Mapped[list[Org]] = relationship(
        secondary=AssociationOrgActivity.__tablename__,
        back_populates="activities",
    )

    def __init__(
        self,
        name: str,
        parent_path: str | Ltree | None = None,
        **kwargs: Any,
    ) -> None:
        if "id" not in kwargs:
            kwargs["id"] = uuid.uuid4()
        super().__init__(**kwargs, name=name)

        if parent_path is not None:
            parent_path = Ltree(parent_path)

        path: Ltree = Ltree(Activity.slugify(self.name))
        self.path: Ltree = path if parent_path is None else parent_path + path

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "name":
            path = Ltree(Activity.slugify(value))
            if self.path is None:
                self.path = path
            parent_path = self.path.lca(self.path)  # type: ignore[arg-type]
            self.path = path if parent_path is None else parent_path + path

    @staticmethod
    def slugify(s: str) -> str:
        s = unidecode.unidecode(s).lower().strip()
        s = re.sub(r"[^\w\s.-]", "", s)
        s = re.sub(r"[\s_-]+", "_", s)
        s = re.sub(r"^-+|-+$", "", s)
        s = re.sub(r"_+", "_", s)
        s = re.sub(r"\.(?=[\w_])", ".", s)
        return s


@dataclass
class Contact(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email_address: Mapped[str | None] = mapped_column(default=None)
    phone_number: Mapped[str | None] = mapped_column(default=None)
    website: Mapped[str | None] = mapped_column(default=None)
    address_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("addressgeo.id"),
        default=None,
    )
    address: Mapped[AddressGeo] = relationship()


@dataclass
class AddressGeo(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
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
