# mypy: ignore-errors
import json
import logging
import os
import sys
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError
from sqlalchemy import inspect
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    class_mapper,
)

logger = logging.getLogger("run_load_fixtures")
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)


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
            try:
                setattr(instance, key, value)
            except AttributeError as e:
                print(f"instance -> {instance}")
                print(f"key -> {key}")
                print(f"value -> {value}")
                raise e

    return instance


def load_entities(
    db: Session,
    data: Any,
    sql_cls: type[DeclarativeBase],
    pyd_cls: type[BaseModel],
    cls_map: dict,
    get_db_instance,
) -> None:
    for instance_data in data:
        try:
            entity_in = pyd_cls.model_validate(instance_data)
        except ValidationError as e:
            logger.error(f"Error processing {sql_cls.__name__}")
            logger.error(f"{e}")
            logger.error(json.dumps(instance_data))
            sys.exit(1)
        instance = populate_model_from_dict(
            sql_cls=sql_cls,
            data=entity_in.model_dump(exclude_none=True),
            cls_map=cls_map,
            get_db_instance=get_db_instance,
        )

        inspector = inspect(instance)
        if inspector.modified:
            logger.info(f"{sql_cls.__name__}: {instance}")
            try:
                db.commit()
            except Exception as e:
                logger.error(f"{e}")
                sys.exit(1)
            db.refresh(instance)
