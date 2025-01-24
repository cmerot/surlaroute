import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.models import Event, Org, Tour
from app.core.security import set_security_context_from_user
from app.users.crud import get_user_by_email


@pytest.mark.usefixtures("entities_with_default_permissions")
def test_default_permissions_unprivileged(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="unprivileged@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_default_permissions")
def test_default_permissions_group_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="group_member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_default_permissions")
def test_default_permissions_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_default_permissions")
def test_default_permissions_owner(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="owner@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_default_permissions")
def test_default_permissions_superuser(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="superuser@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.mark.usefixtures("entities_with_other_read_permission")
def test_other_read_unprivileged(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="unprivileged@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_other_read_permission")
def test_other_read_group_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="group_member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_other_read_permission")
def test_other_read_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_other_read_permission")
def test_other_read_owner(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="owner@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_other_read_permission")
def test_other_read_superuser(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="superuser@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.mark.usefixtures("entities_with_member_read_permission")
def test_member_read_unprivileged(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="unprivileged@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_member_read_permission")
def test_member_read_group_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="group_member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_member_read_permission")
def test_member_read_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_member_read_permission")
def test_member_read_owner(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="owner@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_member_read_permission")
def test_member_read_superuser(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="superuser@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.mark.usefixtures("entities_with_group_member_read_permission")
def test_group_read_unprivileged(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="unprivileged@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_group_member_read_permission")
def test_group_read_group_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="group_member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_group_member_read_permission")
def test_group_read_member(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="member@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 1


@pytest.mark.usefixtures("entities_with_group_member_read_permission")
def test_group_read_owner(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="owner@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 2


@pytest.mark.usefixtures("entities_with_group_member_read_permission")
def test_group_read_superuser(db_session: Session):
    set_security_context_from_user(
        db_session, get_user_by_email(session=db_session, email="superuser@module")
    )

    tours = db_session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = db_session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = db_session.scalars(select(Org)).all()
    assert len(orgs) == 5
