import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.directory import organisation_crud as crud
from app.directory.models import Activity, Organisation
from app.directory.organisation_schemas import OrganisationCreate, OrganisationUpdate
from app.directory.schemas import PageParams
from tests.directory.fixtures import (
    organisation_fixtures,
)


def print_activities(activities: Sequence[Activity]) -> None:
    print("")
    for activity in activities:
        print(f"{activity.path} - {activity.name}")


def test_create_organisation(session: Session) -> None:
    organisation_create = OrganisationCreate(name="org")
    organisation = crud.create_organisation(
        session=session, organisation_create=organisation_create
    )
    assert isinstance(organisation, Organisation)
    assert organisation.name == "org"

    session.rollback()


def test_read_organisation(session: Session) -> None:
    organisation = crud.read_organisation(
        session=session, id=organisation_fixtures[0].id
    )
    assert isinstance(organisation, Organisation)
    assert organisation.id == organisation_fixtures[0].id


def test_read_organisation_not_found(session: Session) -> None:
    with pytest.raises(NoResultFound):
        crud.read_organisation(session=session, id=uuid.uuid4())


def test_read_organisations(session: Session) -> None:
    organisations, count = crud.read_organisations(session=session)
    assert len(organisations) == len(organisation_fixtures)

    page_params = PageParams(limit=1)
    organisations, count = crud.read_organisations(
        session=session, page_params=page_params
    )
    assert len(organisations) == 1


def test_update_organisation(session: Session) -> None:
    organisation_update = OrganisationUpdate(name="new name")
    organisation = crud.update_organisation(
        session=session,
        id=organisation_fixtures[0].id,
        organisation_update=organisation_update,
    )
    assert organisation.name == "new name"

    session.rollback()


def test_update_organisation_not_found(session: Session) -> None:
    organisation_update = OrganisationUpdate(name="new name")
    with pytest.raises(NoResultFound):
        crud.update_organisation(
            session=session,
            id=uuid.uuid4(),
            organisation_update=organisation_update,
        )


def test_delete_organisation(session: Session) -> None:
    org = crud.create_organisation(
        session=session, organisation_create=OrganisationCreate(name="to delete")
    )
    session.commit()
    crud.delete_organisation(session=session, id=org.id)
    session.commit()
    with pytest.raises(NoResultFound):
        crud.read_organisation(session=session, id=org.id)

    session.rollback()
