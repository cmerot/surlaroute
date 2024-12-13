#!/usr/bin/env python
import json
import logging
import sys
import uuid
from typing import Any, TypeVar

from sqlalchemy import ColumnElement, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import (
    DeclarativeBase,
)
from sqlalchemy_utils import Ltree

from app.core.db.models import (
    Activity,
    AddressGeo,
    Base,
    Discipline,
    Event,
    Mobility,
    Org,
    Tour,
    User,
)
from app.core.db.session import SessionLocal
from app.core.security import get_password_hash
from app.directory.crud_schemas import (
    EventImport,
    OrgImport,
    TourImport,
    TreeImport,
    UserImport,
)
from scripts.lib import get_input_file_path, load_entities, set_logger

db = SessionLocal()

T = TypeVar("T", bound=DeclarativeBase)


def create_filter(model: type[T], data: dict[str, Any]) -> ColumnElement[bool] | None:
    """
    used by `get_db_instance` to look for a match with all
    provided varchar or datetime attributes.
    """
    filters = []
    for key, value in data.items():
        if hasattr(model, key) and not isinstance(value, dict | list | set):
            attr = getattr(model, key)
            if str(attr.type) in ["VARCHAR", "DATETIME"]:
                filters.append(attr == value)

    if filters:
        return and_(*filters)
    else:
        return None


def get_db_instance(sql_cls: type[T], data: dict[str, Any]) -> T:
    """
    function used by scripts.lib.load_entities to retrieve an
    already existing instance from database or a new one.

    It'll receive any classes used in the sqlalchemy model
    with it's corresponding data from data and try to find the
    corresponding instance
    """

    # if issubclass(sql_cls, TreeBase):  # mypy complains
    if sql_cls is Activity | Discipline | Mobility:
        """ Specific request for TreeBase classes based on the unique TreeBase.path, 100% sure """
        try:
            instance = (
                db.query(sql_cls).where(sql_cls.path == Ltree(data["path"])).one()  # type: ignore[attr-defined]
            )
        except NoResultFound:
            instance = sql_cls()
            db.add(instance)

        return instance

    elif sql_cls is User:
        """ Specific request for User based on the unique User.email, 100% sure """
        try:
            instance = db.query(sql_cls).filter(User.email == data["email"]).one()
        except NoResultFound:
            instance = sql_cls()
            instance.hashed_password = get_password_hash(str(uuid.uuid4()))  # type: ignore[attr-defined]
            db.add(instance)

        return instance

    elif sql_cls is AddressGeo:
        instance = sql_cls()
        db.add(instance)
        return instance

    try:
        """
        Otherwise we'll match all attributes we have. For instance we have
        two different people named David and we have no more information,
        we'll just match the name. So the first occurence will create a person,
        the second will reuse the first one, instead of creating a new one.
        """
        created_filter = create_filter(sql_cls, data)
        if created_filter is None:
            raise NoResultFound("No data found to create a filter")
        instance = db.query(sql_cls).filter(created_filter).one()
    except NoResultFound:
        instance = sql_cls()
        db.add(instance)
    except Exception as e:
        print("Exception in get_db_instance")
        print(sql_cls.__name__)
        print(data)
        print(str(e))
        sys.exit(1)

    return instance


def get_class_from_name(cls_name: str) -> type[T] | None:
    for mapper in Base.registry.mappers:
        if mapper.class_.__name__ == cls_name:
            return mapper.class_
    return None


if __name__ == "__main__":
    logger = logging.getLogger("load_fixture")
    logging.basicConfig(level=logging.INFO)
    set_logger(logger)

    with open(get_input_file_path()) as f:
        data = json.load(f)
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Activity,
            pyd_cls=TreeImport,
            data=data["activities"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Discipline,
            pyd_cls=TreeImport,
            data=data["disciplines"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Mobility,
            pyd_cls=TreeImport,
            data=data["mobilities"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Org,
            pyd_cls=OrgImport,
            data=data["productions"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=User,
            pyd_cls=UserImport,
            data=data["users"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Tour,
            pyd_cls=TourImport,
            data=data["tours"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Event,
            pyd_cls=EventImport,
            data=data["events"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            sql_cls=Org,
            pyd_cls=OrgImport,
            data=data["ressources"],
        )
