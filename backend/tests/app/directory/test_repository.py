import uuid

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Org, Person, User
from app.directory.repository import get_all_actors, get_org, get_person
from app.directory.schemas import DirectoryPageParams


@pytest.mark.usefixtures("function_create_actors")
def test_get_all_actors(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)

    actors, count = get_all_actors(session=db_session)

    assert len(actors) == 10  # Check if the number of actors is within the limit
    assert count == 20  # Ensure count is returned


@pytest.mark.usefixtures("function_create_actors")
def test_get_all_actors_paginated(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)

    actors, count = get_all_actors(
        session=db_session, page_params=DirectoryPageParams(limit=5)
    )

    assert len(actors) == 5  # Check if the number of actors is within the limit
    assert count == 20  # Ensure count is returned


def test_get_org(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    org = Org(name="test")
    db_session.add(org)
    db_session.flush()
    org = get_org(session=db_session, id=org.id)

    assert org is not None  # Ensure the org is found


def test_get_org_not_found(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    non_existent_id = uuid.uuid4()

    with pytest.raises(NoResultFound):
        get_org(session=db_session, id=non_existent_id)


def test_get_person(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    person = Person(name="test")
    db_session.add(person)
    db_session.flush()
    person = get_person(session=db_session, id=person.id)

    assert person is not None  # Ensure the person is found


def test_get_person_not_found(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    non_existent_id = uuid.uuid4()

    with pytest.raises(NoResultFound):
        get_person(session=db_session, id=non_existent_id)
