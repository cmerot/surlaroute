#!/usr/bin/env python
# mypy: ignore-errors
import json
import sys
import uuid
from typing import Any

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy_utils import Ltree

from app.core.db.models import (
    Activity,
    Discipline,
    Event,
    Mobility,
    Org,
    Person,
    Tour,
    TourActorAssoc,
    TreeBase,
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
from scripts.lib import get_path, load_entities

db = SessionLocal()


def create_filter(model, data):
    """
    used by `get_db_instance` to look for an exact for all
    provided attributes in data.
    """
    filters = []
    for key, value in data.items():
        if hasattr(model, key) and not isinstance(value, dict | list | set):
            attr = getattr(model, key)
            filters.append(attr == value)

    # Combine filters using AND or OR as needed
    # For example, to combine filters with AND:
    if filters:
        return and_(*filters)
    else:
        return None


def get_db_instance(sql_cls: type, data: dict[str, Any]):
    """
    function used by scripts.lib.load_entities to retrieve an
    already existing instance from database or a new one.

    It'll receive any classes used in the sqlalchemy model
    with it's corresponding data from data and try to find the
    corresponding instance
    """

    if issubclass(sql_cls, TreeBase):
        """ Specific request for TreeBase classes based on the unique TreeBase.path, 100% sure """
        try:
            instance = (
                db.query(sql_cls).where(sql_cls.path == Ltree(data["path"])).one()
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
            instance.hashed_password = get_password_hash(str(uuid.uuid4()))
            db.add(instance)
        return instance
    elif sql_cls is TourActorAssoc:
        """
        Specific request for TourActorAssoc classes, 100% sure
        We just need to remove the TourActorAssoc.data which is a JSONB field
        """
        try:
            instance = (
                db.query(sql_cls)
                .filter(
                    create_filter(
                        sql_cls, {k: v for k, v in data.items() if k != "data"}
                    )
                )
                .one()
            )
        except NoResultFound:
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
        instance = db.query(sql_cls).filter(create_filter(sql_cls, data)).one()
    except NoResultFound:
        instance = sql_cls()
        db.add(instance)
    except Exception as e:
        print(sql_cls.__name__)
        print(data)
        print(str(e))
        sys.exit(1)
    return instance


if __name__ == "__main__":
    """
    This is a map to handle polymorphism. To instantiate
    the right subclass we need this mapping, the str part
    being the discrimator in the json data, under the `type_` key.
    In this example, an actor will be instanciated with the Person class:

        { "actor": { "name": "robert", "type_": "Person" } }

    """
    cls_map = {"Person": Person, "Org": Org}

    with open(get_path("../fixtures/private/data.json")) as f:
        data = json.load(f)
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Activity,
            pyd_cls=TreeImport,
            data=data["activities"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Discipline,
            pyd_cls=TreeImport,
            data=data["disciplines"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Mobility,
            pyd_cls=TreeImport,
            data=data["mobilities"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Org,
            pyd_cls=OrgImport,
            data=data["orgs"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Tour,
            pyd_cls=TourImport,
            data=data["tours"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=Event,
            pyd_cls=EventImport,
            data=data["events"],
        )
        load_entities(
            db=db,
            get_db_instance=get_db_instance,
            cls_map=cls_map,
            sql_cls=User,
            pyd_cls=UserImport,
            data=data["users"],
        )
