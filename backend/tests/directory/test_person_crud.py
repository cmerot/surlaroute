import uuid

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Person
from app.core.schemas import (
    PageParams,
)
from app.directory import crud
from app.directory.crud_schemas import PersonCreate, PersonUpdate
from tests.directory.fixtures import (
    person_fixtures,
)


def test_create_person(session: Session) -> None:
    person_create = PersonCreate(name="rob mitch")
    person = crud.create_person(session=session, person_create=person_create)
    assert isinstance(person, Person)
    assert person.name == "rob mitch"

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
    person_update = PersonUpdate(name="new name")
    person = crud.update_person(
        session=session,
        id=person_fixtures[0].id,
        person_update=person_update,
    )
    assert person.name == "new name"

    session.rollback()


def test_update_person_not_found(session: Session) -> None:
    person_update = PersonUpdate(name="new name")
    with pytest.raises(NoResultFound):
        crud.update_person(
            session=session,
            id=uuid.uuid4(),
            person_update=person_update,
        )


def test_delete_person(session: Session) -> None:
    org = crud.create_person(
        session=session, person_create=PersonCreate(name="to delete")
    )
    session.commit()
    crud.delete_person(session=session, id=org.id)
    session.commit()
    with pytest.raises(NoResultFound):
        crud.read_person(session=session, id=org.id)

    session.rollback()
