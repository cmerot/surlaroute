import json
import logging
import os
import sys
from collections.abc import Callable
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    class_mapper,
)

from app.core.db.models import Base

"""
populate_model_from_dict uses this level to show more info
"""
TRACE_LOG_LEVEL = 5
logging.addLevelName(TRACE_LOG_LEVEL, "TRACE")

logger = logging.getLogger(__name__)


def set_logger(new_logger: logging.Logger) -> None:
    """
    Overrides the global logger, so it can be used in this file
    """
    global logger
    logger = new_logger


def get_input_file_path() -> str:
    # Check if an argument was provided
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_path>")
        sys.exit(1)

    input_file_path = os.path.abspath(sys.argv[1])

    # Check if the file exists
    if not os.path.isfile(input_file_path):
        print(f"Error: The file '{input_file_path}' was not found.")
        sys.exit(1)

    return input_file_path


T = TypeVar("T", bound=DeclarativeBase)


def get_class_from_name(cls_name: str) -> type[T]:
    for mapper in Base.registry.mappers:
        if mapper.class_.__name__ == cls_name:
            return mapper.class_
    raise Exception("polymorphic subclass not found")


def get_submodel_class(
    sql_cls: type[T],
    value: dict[str, Any],
) -> type[T]:
    mapper = class_mapper(sql_cls)
    if mapper.polymorphic_identity is None:
        return sql_cls

    return get_class_from_name(value["type"])


def populate_model_from_dict(
    get_db_instance: Callable[[type[T], dict[str, Any]], T],
    cls: type[T],
    data: dict[str, Any],
    instance: T | None = None,
    level: int = -1,
) -> T | list[T]:
    level += 1

    if instance is None:
        instance = get_db_instance(cls, data)

    logger.log(
        5,
        f"I   {' ' * level * 2}{instance}",
    )

    for data_key, data_attr in data.items():
        cls_attr = getattr(cls, data_key, None)

        # attribute in not present in the model => skip
        if not cls_attr:
            continue

        instance_attr = getattr(instance, data_key)
        # attribute value does not change => skip
        if instance_attr == data_attr:
            continue

        # Relationship
        relationship = cls.__mapper__.relationships.get(data_key)
        if relationship:
            attr_cls = cls_attr.property.mapper.class_
            collection_cls = relationship.collection_class
            if collection_cls:
                """
                We recreate all relations in a new collection
                and we simply replace that collection.
                Eg: if instance is an Org, here we will handle
                Org.member_assocs.
                This will touch all instances in the collection.
                """

                populated_instances = []
                for item in data_attr:
                    populated_instances.append(
                        populate_model_from_dict(
                            get_db_instance=get_db_instance,
                            cls=get_submodel_class(attr_cls, item),
                            data=item,
                            instance=None,
                            level=level,
                        )
                    )

                logger.log(
                    TRACE_LOG_LEVEL,
                    f"R[] {' ' * level * 2}{cls.__name__}.{data_key}: {instance_attr}",
                )
                setattr(instance, data_key, populated_instances)

            else:
                logger.log(
                    TRACE_LOG_LEVEL,
                    f"R   {' ' * level * 2}{cls.__name__}.{data_key}: {instance_attr}",
                )
                populated_instance = populate_model_from_dict(
                    get_db_instance=get_db_instance,
                    cls=get_submodel_class(attr_cls, data_attr),
                    data=data_attr,
                    instance=instance_attr,
                    level=level,
                )

                if instance_attr != populated_instance:
                    setattr(instance, data_key, populated_instance)

        # Column attribute
        else:
            if isinstance(cls_attr.type, JSONB):
                data_attr = json.loads(data_attr)
            logger.log(
                TRACE_LOG_LEVEL,
                f"C   {' ' * level * 2}{cls.__name__}.{data_key}: {data_attr}",
            )
            setattr(instance, data_key, data_attr)

    return instance


def add_polymorphic_discriminator(
    d: dict[str, Any] | list[Any],
) -> dict[str, Any] | list[Any]:
    """
    Add the polymorphic discriminator to the data:
    Replace
        {"actor#Person": {"name": "value"}}
    by
        {"actor": {"name": "value", "type": "Person"}}
    """
    if isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            if "#" in key:
                new_key, type_value = key.split("#", 1)
                new_dict[new_key] = value
                new_dict[new_key]["type"] = type_value
            elif isinstance(value, dict | list):
                new_dict[key] = add_polymorphic_discriminator(value)
            else:
                new_dict[key] = value
        return new_dict
    elif isinstance(d, list):
        return [add_polymorphic_discriminator(item) for item in d]
    else:
        return d


def load_entities(
    db: Session,
    data: Any,
    sql_cls: type[T],
    pyd_cls: type[BaseModel],
    get_db_instance: Callable[[type[T], dict[str, Any]], T],
) -> None:
    data = add_polymorphic_discriminator(data)
    for instance_data in data:
        try:
            entity_in = pyd_cls.model_validate(instance_data)
        except ValidationError as e:
            logger.error(f"Error validating data for {sql_cls.__name__}")
            logger.error(f"{e}")
            logger.error(json.dumps(instance_data))
            sys.exit(1)

        logger.log(
            TRACE_LOG_LEVEL,
            "Legend: I=>instance, R=>relationship, R[]=>m2m relationship, C=>column",
        )
        instance = populate_model_from_dict(
            cls=sql_cls,
            data=entity_in.model_dump(exclude_none=True),
            get_db_instance=get_db_instance,
        )

        new_instances = db.new
        dirty_instances = db.dirty
        deleted_instances = db.deleted

        if (
            len(new_instances) > 0
            or len(dirty_instances) > 0
            or len(deleted_instances) > 0
        ):
            logger.info(f"update {instance}")

        for new_instance in new_instances:
            logger.debug(f"- new {new_instance}")
        for dirty_instance in dirty_instances:
            logger.debug(f"- dirty {dirty_instance}")
        for deleted_instance in deleted_instances:
            logger.debug(f"- deleted {deleted_instance}")

        try:
            db.commit()
        except Exception as e:
            logger.error(f"{e}")
            sys.exit(1)
        db.refresh(instance)
