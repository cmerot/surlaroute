import uuid
from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.db.models import Org
from app.core.schemas import PageParams
from app.directory.org_schemas import (
    OrgCreate,
    OrgUpdate,
)


def create_org(
    *,
    session: Session,
    org_create: OrgCreate,
) -> Org:
    db_obj = Org(**org_create.model_dump())
    session.add(db_obj)
    session.flush()
    return db_obj


def read_org(
    *,
    session: Session,
    id: uuid.UUID,
) -> Org:
    return session.get_one(Org, id)


def read_orgs(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Org], int]:
    count_statement = select(func.count()).select_from(Org)
    statement = select(Org).offset(page_params.offset).limit(page_params.limit)

    if page_params.q:
        where_clause = or_(
            Org.name.icontains(page_params.q),
        )
        count_statement = count_statement.where(where_clause)
        statement = statement.where(where_clause)

    count = session.scalars(count_statement).one()
    orgs = session.scalars(statement).all()
    return orgs, count


def update_org(
    *,
    session: Session,
    id: uuid.UUID,
    org_update: OrgUpdate,
) -> Org:
    org = session.get_one(Org, id)
    for key, value in org_update.model_dump(exclude_unset=True).items():
        setattr(org, key, value)
    session.add(org)
    session.flush()
    return org


def delete_org(*, session: Session, id: uuid.UUID) -> None:
    org = session.get_one(Org, id)
    session.delete(org)
    session.flush()
