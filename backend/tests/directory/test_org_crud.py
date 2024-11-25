import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Activity, Org
from app.directory import org_crud as crud
from app.directory.org_schemas import OrgCreate, OrgUpdate
from app.directory.schemas import PageParams
from tests.directory.fixtures import (
    org_fixtures,
)


def print_activities(activities: Sequence[Activity]) -> None:
    print("")
    for activity in activities:
        print(f"{activity.path} - {activity.name}")


def test_create_org(session: Session) -> None:
    org_create = OrgCreate(name="org")
    org = crud.create_org(session=session, org_create=org_create)
    assert isinstance(org, Org)
    assert org.name == "org"

    session.rollback()


def test_read_org(session: Session) -> None:
    org = crud.read_org(session=session, id=org_fixtures[0].id)
    assert isinstance(org, Org)
    assert org.id == org_fixtures[0].id


def test_read_org_not_found(session: Session) -> None:
    with pytest.raises(NoResultFound):
        crud.read_org(session=session, id=uuid.uuid4())


def test_read_orgs(session: Session) -> None:
    orgs, count = crud.read_orgs(session=session)
    assert len(orgs) == len(org_fixtures)

    page_params = PageParams(limit=1)
    orgs, count = crud.read_orgs(session=session, page_params=page_params)
    assert len(orgs) == 1


def test_update_org(session: Session) -> None:
    org_update = OrgUpdate(name="new name")
    org = crud.update_org(
        session=session,
        id=org_fixtures[0].id,
        org_update=org_update,
    )
    assert org.name == "new name"

    session.rollback()


def test_update_org_not_found(session: Session) -> None:
    org_update = OrgUpdate(name="new name")
    with pytest.raises(NoResultFound):
        crud.update_org(
            session=session,
            id=uuid.uuid4(),
            org_update=org_update,
        )


def test_delete_org(session: Session) -> None:
    org = crud.create_org(session=session, org_create=OrgCreate(name="to delete"))
    session.commit()
    crud.delete_org(session=session, id=org.id)
    session.commit()
    with pytest.raises(NoResultFound):
        crud.read_org(session=session, id=org.id)

    session.rollback()
