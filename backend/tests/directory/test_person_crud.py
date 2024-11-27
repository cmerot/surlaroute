import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Activity, Person
from app.core.schemas import (
    PageParams,
)
from app.directory import crud
from app.directory.crud_schemas import PersonCreate, PersonUpdate
from tests.directory.fixtures import (
    person_fixtures,
)


def print_activities(activities: Sequence[Activity]) -> None:
    print("")
    for activity in activities:
        print(f"{activity.path} - {activity.name}")


def test_create_person(session: Session) -> None:
    person_create = PersonCreate(firstname="rob", lastname="mitch")
    person = crud.create_person(session=session, person_create=person_create)
    assert isinstance(person, Person)
    assert person.firstname == "rob"

    session.rollback()


def test_read_person(session: Session) -> None:
    person = crud.read_person(session=session, id=person_fixtures[0].id)
    assert isinstance(person, Person)
    assert person.id == person_fixtures[0].id


def test_read_person_not_found(session: Session) -> None:
    with pytest.raises(NoResultFound):
        crud.read_person(session=session, id=uuid.uuid4())


def test_read_people(session: Session) -> None:
    people, count = crud.read_people(session=session)
    assert len(people) == len(person_fixtures)

    page_params = PageParams(limit=1)
    people, count = crud.read_people(session=session, page_params=page_params)
    assert len(people) == 1


def test_update_person(session: Session) -> None:
    person_update = PersonUpdate(firstname="new name")
    person = crud.update_person(
        session=session,
        id=person_fixtures[0].id,
        person_update=person_update,
    )
    assert person.firstname == "new name"

    session.rollback()


def test_update_person_not_found(session: Session) -> None:
    person_update = PersonUpdate(firstname="new name")
    with pytest.raises(NoResultFound):
        crud.update_person(
            session=session,
            id=uuid.uuid4(),
            person_update=person_update,
        )


def test_delete_person(session: Session) -> None:
    org = crud.create_person(
        session=session, person_create=PersonCreate(firstname="to", lastname="delete")
    )
    session.commit()
    crud.delete_person(session=session, id=org.id)
    session.commit()
    with pytest.raises(NoResultFound):
        crud.read_person(session=session, id=org.id)

    session.rollback()
