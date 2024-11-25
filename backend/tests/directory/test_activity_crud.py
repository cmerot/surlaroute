from collections.abc import Sequence

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Activity
from app.directory import activity_crud as crud
from app.directory.activity_schemas import (
    ActivityCreate,
    ActivityUpdate,
)
from tests.directory.fixtures import (
    activity_fixtures,
)


def print_activities(activities: Sequence[Activity]) -> None:
    print("")
    for activity in activities:
        print(f"{activity.path} - {activity.name}")


def test_create_activity(session: Session) -> None:
    activity_create = ActivityCreate(name="dog")
    activity = crud.create_activity(session=session, activity_create=activity_create)
    assert isinstance(activity, Activity)
    assert activity.name == "dog"
    assert str(activity.path) == "dog"

    session.rollback()


def test_create_activity_parent_path(session: Session) -> None:
    activity_create = ActivityCreate(name="small", parent_path="dog")
    activity = crud.create_activity(session=session, activity_create=activity_create)
    assert isinstance(activity, Activity)
    assert activity.name == "small"
    assert str(activity.path) == "dog.small"

    session.rollback()


def test_read_activity(session: Session) -> None:
    activity = crud.read_activity(session=session, path="cat.small")
    assert isinstance(activity, Activity)
    assert activity.name == "small"
    assert str(activity.path) == "cat.small"

    session.rollback()


def test_read_activity_not_found(session: Session) -> None:
    with pytest.raises(NoResultFound):
        crud.read_activity(session=session, path="do.not.exist")

        session.rollback()


def test_read_activities_no_path(session: Session) -> None:
    activities, count = crud.read_activities(session=session)
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"

    session.rollback()


def test_read_activities_path_none(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path=None)
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"

    session.rollback()


def test_read_activities_path_empty_string(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="")
    assert isinstance(activities, Sequence)
    assert len(activities) == len(activity_fixtures)
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat"
    assert str(activities[-1].path) == "cat.small.wild.ocelot"

    session.rollback()


def test_read_activities_deep(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="cat.big")
    assert isinstance(activities, Sequence)
    assert len(activities) == 4
    assert isinstance(activities[0], Activity)
    assert str(activities[0].path) == "cat.big"
    assert str(activities[-1].path) == "cat.big.tiger"

    session.rollback()


def test_read_activities_not_found(session: Session) -> None:
    activities, count = crud.read_activities(session=session, path="do.not.exist")
    assert isinstance(activities, Sequence)
    assert len(activities) == 0

    session.rollback()


def test_update_activity_name(session: Session) -> None:
    path = "cat.small"
    activity_update = ActivityUpdate(name="small2")
    crud.update_activity(session=session, path=path, activity_update=activity_update)
    activities, count = crud.read_activities(session=session, path="cat.small2")
    assert len(activities) == 8
    assert activities[0].name == "small2"

    session.rollback()


def test_update_activity_path(session: Session) -> None:
    path = "cat.small"
    activity_update = ActivityUpdate(parent_path="cat.big")
    crud.update_activity(session=session, path=path, activity_update=activity_update)
    activities, count = crud.read_activities(session=session, path="cat.big.small")
    assert len(activities) == 8

    session.rollback()


def test_update_activity_path_and_name(session: Session) -> None:
    path = "cat.small"
    activity_update = ActivityUpdate(parent_path="cat.big", name="small2")
    crud.update_activity(session=session, path=path, activity_update=activity_update)
    activities, count = crud.read_activities(session=session, path="cat.big.small2")
    assert len(activities) == 8

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
