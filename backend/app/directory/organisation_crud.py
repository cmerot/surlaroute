import uuid
from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.directory.models import Organisation
from app.directory.organisation_schemas import (
    OrganisationCreate,
    OrganisationUpdate,
)
from app.directory.schemas import PageParams
from tests.directory.test_models import print_actor


def create_organisation(
    *,
    session: Session,
    organisation_create: OrganisationCreate,
) -> Organisation:
    db_obj = Organisation(**organisation_create.model_dump())
    session.add(db_obj)
    return db_obj


def read_organisation(
    *,
    session: Session,
    id: uuid.UUID,
) -> Organisation:
    return session.get_one(Organisation, id)


def read_organisations(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Organisation], int]:
    count_statement = select(func.count()).select_from(Organisation)
    statement = select(Organisation).offset(page_params.offset).limit(page_params.limit)

    if page_params.q:
        where_clause = or_(
            Organisation.name.contains(page_params.q),
        )
        count_statement = count_statement.where(where_clause)
        statement = statement.where(where_clause)

    count = session.scalars(count_statement).one()
    orgs = session.scalars(statement).all()
    for o in orgs:
        print_actor(o)
    return orgs, count


def update_organisation(
    *,
    session: Session,
    id: uuid.UUID,
    organisation_update: OrganisationUpdate,
) -> Organisation:
    org = session.get_one(Organisation, id)
    for key, value in organisation_update.model_dump().items():
        setattr(org, key, value)
    return org


def delete_organisation(*, session: Session, id: uuid.UUID) -> None:
    org = session.get_one(Organisation, id)
    session.delete(org)
    session.flush()
