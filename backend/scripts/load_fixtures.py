#!/usr/bin/env python
# type: ignore
import json
import logging
import sys
import uuid
from typing import Any, TypeVar

from sqlalchemy import ColumnElement, and_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import (
    DeclarativeBase,
)
from sqlalchemy_utils import Ltree

from app.core.db.models import (
    Activity,
    AddressGeo,
    Discipline,
    Event,
    Mobility,
    Org,
    Tour,
    TreeBase,
    User,
)
from app.core.db.session import get_db
from app.core.security import get_password_hash
from scripts.import_schemas import (
    EventImport,
    OrgImport,
    TourImport,
    TreeImport,
    UserImport,
)
from scripts.lib import get_input_file_path, load_entities, set_logger

db = next(get_db())

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
    already existing instance from database or instantiate a new one.

    It'll receive any class from the registry with its corresponding
    data and try to find the corresponding instance.

    The default case is to match all attributes we have but there are
    exceptions.
    """

    # if sql_cls is Activity | Discipline | Mobility:
    if issubclass(sql_cls, TreeBase):  # mypy complains
        """ Specific request for TreeBase classes based on the unique TreeBase.path """
        try:
            instance = (
                db.query(sql_cls).where(sql_cls.path == Ltree(data["path"])).one()  # type: ignore[attr-defined]
            )
        except NoResultFound:
            instance = sql_cls()
            db.add(instance)

        return instance

    elif sql_cls is User:
        """ Specific request for User based on the unique User.email """
        try:
            instance = db.query(sql_cls).filter(User.email == data["email"]).one()
        except NoResultFound:
            instance = sql_cls()
            instance.hashed_password = get_password_hash(str(uuid.uuid4()))  # type: ignore[attr-defined]
            db.add(instance)

        return instance

    elif sql_cls is AddressGeo:
        """
        This class is only used in a one-to-one relationship with Contact
        so either we have an instance already populated and we don't need to match
        or it's a new Contact with a new AddressGeo.

        It cannot be handled by the default handler because we need an instance per Contact
        and 2 AddressGeo can be exactly the same, so there is no point in looking for a match.
        """
        instance = sql_cls()
        db.add(instance)
        return instance

    try:
        """
        Default case: we'll match all attributes we have.

        In can be a problem in many cases, for instance we have
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


if __name__ == "__main__":
    logger = logging.getLogger("load_fixture")
    logging.basicConfig(level=20)
    set_logger(logger)

    user = db.scalar(select(User).where(User.email == "admin@example.com"))
    db.info["user"] = user

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
