import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import unidecode
from sqlalchemy import DateTime, ForeignKey, func
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


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


@dataclass
class OrganisationMembers(Base, TimestampMixin):
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id"), primary_key=True
    )
    actor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"), primary_key=True
    )
    membership_data: Mapped[str] = mapped_column(default="")
    actor: Mapped["Actor"] = relationship(
        back_populates="memberships", foreign_keys=[actor_id]
    )
    organisation: Mapped["Organisation"] = relationship(
        back_populates="members", foreign_keys=[organisation_id]
    )

    def __repr__(self) -> str:
        return f"OrganisationMembers({self.actor} in {self.organisation})"


@dataclass
class Actor(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    memberships: Mapped[list["OrganisationMembers"]] = relationship(
        cascade="all, delete-orphan",
    )
    type: Mapped[str] = mapped_column()

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


class Organisation(Actor, TimestampMixin):
    id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("actor.id"),
        primary_key=True,
    )
    name: Mapped[str]
    members: Mapped[list["OrganisationMembers"]] = relationship(
        back_populates="organisation",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Person(Actor, TimestampMixin):
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
    path: Mapped[Ltree] = mapped_column(LtreeType, unique=True)
    parent: Mapped["Activity"] = relationship(
        "Activity",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    def __init__(
        self,
        parent_path: str | Ltree | None = None,
        **kwargs: Any,
    ) -> None:
        if "id" not in kwargs:
            kwargs["id"] = uuid.uuid4()
        super().__init__(**kwargs)

        if parent_path is not None:
            parent_path = Ltree(parent_path)

        path: Ltree = Ltree(self.name)
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
