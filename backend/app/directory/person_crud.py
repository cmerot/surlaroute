import uuid
from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db.models import Person
from app.core.schemas import PageParams
from app.directory.person_schemas import PersonCreate, PersonUpdate


def create_person(*, session: Session, person_create: PersonCreate) -> Person:
    db_obj = Person(**person_create.model_dump())
    session.add(db_obj)
    session.flush()
    return db_obj


def read_person(*, session: Session, id: uuid.UUID) -> Person:
    return session.get_one(Person, id)


def read_people(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Person], int]:
    count_statement = select(func.count()).select_from(Person)
    statement = select(Person).offset(page_params.offset).limit(page_params.limit)
    count = session.scalars(count_statement).one()
    orgs = session.scalars(statement).all()
    return orgs, count


def update_person(
    *,
    session: Session,
    id: uuid.UUID,
    person_update: PersonUpdate,
) -> Person:
    person = session.get_one(Person, id)
    for key, value in person_update.model_dump(exclude_unset=True).items():
        setattr(person, key, value)
    session.add(person)
    session.flush()
    return person


def delete_person(*, session: Session, id: uuid.UUID) -> None:
    person = session.get_one(Person, id)
    session.delete(person)
    session.flush()
