#!/usr/bin/env python
# mypy: ignore-errors
import json
import os
import sys
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    class_mapper,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy_utils import Ltree

from app.core.db.models import (
    Activity,
    Discipline,
    Event,
    Mobility,
    Org,
    Person,
    Tour,
    TreeBase,
)
from app.core.db.session import SessionLocal
from app.directory.crud_schemas import (
    EventImport,
    OrgImport,
    TourImport,
    TreeImport,
)

db = SessionLocal()


def get_path(relative_path: str) -> str:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path
    full_path = os.path.join(script_dir, relative_path)
    return full_path


T = TypeVar("T")


def populate_model_from_dict(
    sql_cls: type[T],
    data: dict,
    cls_map: dict[str, type],
    get_db_instance: Callable[[type, dict], T | None],
) -> T:
    """
    Populates a model instance from a dictionary, retrieving data from the database first.
    It handles some kind of relations and polymorphism. To handle polymorphism, a discriminator
    is used in the data. Eg. {"actor": {"firstname": "rob", "type_": "Person"}}.

    Args:
        session: an sqlalchemy Session
        model_class: The model class to instantiate.
        data: The dictionary containing the data to populate the model.
        model_map: Dictionary mapping model names to their corresponding child models.
        get_db_obj_func: A function to retrieve an existing database object based on the model class and data.

    Returns:
        An instance of the model populated with the data.
    """

    def get_submodel_class(sql_cls: type, value: dict):
        mapper = class_mapper(sql_cls)
        if mapper.polymorphic_identity is None:
            return sql_cls
        try:
            return cls_map.get(value["type_"], sql_cls)
        except KeyError:
            return sql_cls

    instance = get_db_instance(sql_cls, data)

    # Instance is not new
    if instance.__dict__["_sa_instance_state"].key is not None:
        # Remove keys from data that are already in db_instance
        data = {
            k: v
            for k, v in data.items()
            if hasattr(instance, k) and getattr(instance, k) != v
        }

    for key, value in data.items():
        attr = getattr(sql_cls, key, None)
        if attr and isinstance(attr, InstrumentedAttribute):
            if isinstance(value, dict | list | set):
                # For a collection
                if isinstance(value, list) or isinstance(value, set):
                    sub_instances = []
                    for item in value:
                        sub_instance = populate_model_from_dict(
                            sql_cls=get_submodel_class(
                                sql_cls=attr.property.mapper.class_, value=item
                            ),
                            data=item,
                            cls_map=cls_map,
                            get_db_instance=get_db_instance,
                        )
                        sub_instances.append(sub_instance)
                # For a dict
                else:
                    sub_instance = populate_model_from_dict(
                        sql_cls=get_submodel_class(attr.property.mapper.class_, value),
                        data=value,
                        cls_map=cls_map,
                        get_db_instance=get_db_instance,
                    )
                    sub_instances = sub_instance

                setattr(instance, key, sub_instances)
            else:
                setattr(instance, key, value)
        else:
            setattr(instance, key, value)

    return instance


def create_filter(model, data):
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


def get_db_instance(sql_cls: type, data: dict):
    if issubclass(sql_cls, TreeBase):
        try:
            instance = (
                db.query(sql_cls).where(sql_cls.path == Ltree(data["path"])).one()
            )
        except NoResultFound:
            instance = sql_cls()
            db.add(instance)
        return instance

    try:
        instance = db.query(sql_cls).filter(create_filter(sql_cls, data)).one()
    except NoResultFound:
        instance = sql_cls()
        db.add(instance)
    return instance


def load_entities(
    db: Session,
    data: Any,
    sql_cls: type[DeclarativeBase],
    pyd_cls: type[BaseModel],
    cls_map: dict,
) -> None:
    for entity_obj in data:
        print(f"Processing {sql_cls.__name__}")
        try:
            entity_in = pyd_cls.model_validate(entity_obj)
        except Exception:
            print("Impossible d'importer cet élément:")
            print(entity_obj)
            sys.exit(1)
        entity = populate_model_from_dict(
            sql_cls=sql_cls,
            data=entity_in.model_dump(exclude_none=True),
            cls_map=cls_map,
            get_db_instance=get_db_instance,
        )
        db.add(entity)
        db.commit()
        db.refresh(entity)


cls_map = {"Person": Person}

if __name__ == "__main__":
    with open(get_path("../fixtures/private/data.json")) as f:
        data = json.load(f)
        load_entities(
            db=db,
            sql_cls=Activity,
            pyd_cls=TreeImport,
            cls_map=cls_map,
            data=data["activities"],
        )
        load_entities(
            db=db,
            sql_cls=Discipline,
            pyd_cls=TreeImport,
            cls_map=cls_map,
            data=data["disciplines"],
        )
        load_entities(
            db=db,
            sql_cls=Mobility,
            pyd_cls=TreeImport,
            cls_map=cls_map,
            data=data["mobilities"],
        )
        load_entities(
            db=db,
            sql_cls=Org,
            pyd_cls=OrgImport,
            cls_map=cls_map,
            data=data["orgs"],
        )
        load_entities(
            db=db,
            sql_cls=Tour,
            pyd_cls=TourImport,
            cls_map=cls_map,
            data=data["tours"],
        )
        load_entities(
            db=db,
            sql_cls=Event,
            pyd_cls=EventImport,
            cls_map=cls_map,
            data=data["events"],
        )
