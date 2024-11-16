import re
import uuid
from dataclasses import dataclass
from typing import Any

import unidecode
from pydantic import EmailStr
from sqlalchemy import Column, DateTime, ForeignKey, Index, func, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import (
    Mapped,
    foreign,
    mapped_column,
    relationship,
    remote,
)
from sqlalchemy_utils import Ltree, LtreeType
from sqlmodel import Field, SQLModel
from sqlmodel.main import default_registry

from app.api.deps import SessionDep

Base = default_registry.generate_base()


# Person
class PersonBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(min_length=3, max_length=40)


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    email: str | None = Field(default=None, min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=3, max_length=40)


class Person(PersonBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PersonPublic(PersonBase):
    id: uuid.UUID
    name: str
    email: str


class PeoplePublic(SQLModel):
    data: list[PersonPublic]
    count: int


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class OrgActorAssociation(Base, TimestampMixin):
    __tablename__ = "org_actor_association"
    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisation.id"), primary_key=True
    )
    actor_id: Mapped[int] = mapped_column(ForeignKey("actor.id"), primary_key=True)
    extra_data: Mapped[str]
    actor: Mapped["Actor"] = relationship(
        back_populates="memberships", foreign_keys=[actor_id]
    )
    organisation: Mapped["Organisation"] = relationship(
        back_populates="members", foreign_keys=[organisation_id]
    )


class Actor(Base):
    __tablename__ = "actor"
    id: Mapped[int] = mapped_column(primary_key=True)
    memberships: Mapped[list["OrgActorAssociation"]] = relationship(
        back_populates="actor"
    )
    type: Mapped[str] = mapped_column()

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        if cls.__name__ == "Actor":
            return {"polymorphic_on": cls.type, "polymorphic_identity": cls.__name__}
        else:
            return {"polymorphic_identity": cls.__name__}

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


class Organisation(Actor, TimestampMixin):
    __tablename__ = "organisation"
    id: Mapped[int] = mapped_column(ForeignKey("actor.id"), primary_key=True)
    name: Mapped[str]
    members: Mapped[list["OrgActorAssociation"]] = relationship(
        back_populates="organisation",
    )


def slugify(s):
    s = unidecode.unidecode(s).lower().strip()
    s = re.sub(r"[^\w\s.-]", "", s)
    s = re.sub(r"[\s_-]+", "_", s)
    s = re.sub(r"^-+|-+$", "", s)
    s = re.sub(r"_+", "_", s)
    s = re.sub(r"\.(?=[\w_])", ".", s)
    return s


@dataclass
class ActivityRepository:
    session: SessionDep

    def move(self, source: Ltree, dest: Ltree | None) -> tuple[Ltree | None, int]:
        try:
            source = Ltree(source)
            dest = "" if dest is None else Ltree(dest)
        except ValueError as e:
            raise ValueError(f"{e}")

        statement = text(
            f"UPDATE {Activity.__tablename__} "
            f"SET {Activity.path.key} = "
            f"'{dest}' || subpath({Activity.path.key}, nlevel('{source}') - 1) "
            f"WHERE {Activity.path.key} <@ '{source}';"
        )

        try:
            cursor = self.session.exec(statement)
        except Exception as e:
            self.session.rollback()
            raise e
        self.session.commit()

        if dest == "":
            lca = None
        else:
            lca = source.lca(dest)

        return lca, cursor.rowcount


@dataclass
class Activity(Base):
    __tablename__ = "activity"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    path: Mapped[Ltree] = mapped_column(LtreeType, unique=True)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == "name":
            ltree_id = Ltree(slugify(value))
            if self.parent is None:
                self.path = ltree_id
            else:
                self.path = self.parent.path + ltree_id

    parent: Mapped["Activity"] = relationship(
        "Activity",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    def __init__(
        self,
        id: uuid.UUID | None = uuid.uuid4(),
        parent_path: str | Ltree = None,
        **kwargs,
    ):
        super().__init__(**kwargs, id=id)

        if parent_path and isinstance(parent_path, str):
            parent_path = Ltree(parent_path)
        ltree_id = Ltree(slugify(self.name))
        self.path = ltree_id if parent_path is None else parent_path + ltree_id

    __table_args__ = (Index("ix_activity_path", path, postgresql_using="gist"),)
