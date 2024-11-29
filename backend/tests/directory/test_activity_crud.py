from collections.abc import Sequence

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Activity
from app.directory import crud
from app.directory.crud_schemas import (
    TreeCreate,
    TreeUpdate,
)
from tests.directory.fixtures import (
    activity_fixtures,
)


def test_create_activity(session: Session) -> None:
    entity_in = TreeCreate(path="dog")
    activity = crud.create_activity(session=session, entity_in=entity_in)
    assert isinstance(activity, Activity)
    assert activity.name == "dog"
    assert str(activity.path) == "dog"

    entity_in = TreeCreate(path="dog", name="Dog")
    activity = crud.create_activity(session=session, entity_in=entity_in)
    assert isinstance(activity, Activity)
    assert activity.name == "Dog"
    assert str(activity.path) == "dog"

    entity_in = TreeCreate(path="dog.small", name="Small Dog")
    activity = crud.create_activity(session=session, entity_in=entity_in)
    assert isinstance(activity, Activity)
    assert activity.name == "Small Dog"
    assert str(activity.path) == "dog.small"

    session.rollback()


def test_read_activity(session: Session) -> None:
    activity = crud.read_activity(session=session, path="cat.small")
    assert isinstance(activity, Activity)
    assert activity.name == "small"
    assert str(activity.path) == "cat.small"


def test_read_activity_not_found(session: Session) -> None:
    with pytest.raises(NoResultFound):
        crud.read_activity(session=session, path="do.not.exist")


def test_read_activities_no_path(session: Session) -> None:
    activities, count = crud.read_activities(session=session)
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"


def test_read_activities_path_none(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path=None)
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"


def test_read_activities_path_empty_string(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="")
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"


def test_read_activities_deep(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="cat.big")
    assert isinstance(activities, Sequence)
    assert len(activities) == 4
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat.big"
    assert str(activities[-1].path) == "cat.big.tiger"


def test_read_activities_not_found(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="do.not.exist")
    assert isinstance(activities, Sequence)
    assert len(activities) == 0


def test_update_activity_name(session: Session) -> None:
    path = "cat.small"
    entity_in = TreeUpdate(name="small2")
    crud.update_activity(session=session, path=path, entity_in=entity_in)
    activities, count = crud.read_activities(session=session, path="cat.small")
    assert activities[0].name == "small2"

    session.rollback()


def test_update_activity_path(session: Session) -> None:
    path = "cat.small"
    entity_in = TreeUpdate(dest_path="cat.big.small")
    crud.update_activity(session=session, path=path, entity_in=entity_in)
    activities, count = crud.read_activities(session=session, path="cat.big.small")
    assert len(activities) == 8

    path = "cat"
    entity_in = TreeUpdate(dest_path="cats")
    crud.update_activity(session=session, path=path, entity_in=entity_in)
    activities, count = crud.read_activities(session=session, path="cats")
    assert len(activities) == 13

    session.rollback()


def test_update_activity_path_and_name(session: Session) -> None:
    path = "cat.small"
    entity_in = TreeUpdate(dest_path="cat.big.small", name="big small")
    crud.update_activity(session=session, path=path, entity_in=entity_in)
    activities, count = crud.read_activities(session=session, path="cat.big.small")
    assert len(activities) == 8
    assert activities[0].name == "big small"

    session.rollback()


def test_delete_activity(session: Session) -> None:
    rowcount = crud.delete_activity(session=session, path="cat.small")
    assert rowcount == 8

    with pytest.raises(NoResultFound):
        crud.read_activity(session=session, path="cat.small")
    with pytest.raises(NoResultFound):
        crud.read_activity(session=session, path="cat.small.wild")

    session.rollback()


def test_delete_activity_not_found(session: Session) -> None:
    rowcount = crud.delete_activity(session=session, path="do.not.exist")
    assert rowcount == 0

    session.rollback()
