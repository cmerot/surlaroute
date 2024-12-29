import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.models import Event, Org, OrgActorAssoc, Person, Tour, User
from app.users.crud import get_user_by_email


def iid(name: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_OID, name)


def create_person(
    session: Session,
    name: str,
    owner_id: uuid.UUID | None = None,
    group_owner_id: uuid.UUID | None = None,
    other_read: bool = False,
    group_read: bool = False,
    member_read: bool = False,
) -> Person:
    person = Person(
        id=iid(f"{name}_person"),
        name=name,
        owner_id=owner_id,
        group_owner_id=group_owner_id,
        other_read=other_read,
        group_read=group_read,
        member_read=member_read,
    )
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


def create_org(
    session: Session,
    name: str,
    owner_id: uuid.UUID | None = None,
    group_owner_id: uuid.UUID | None = None,
    other_read: bool = False,
    group_read: bool = False,
    member_read: bool = False,
) -> Org:
    org = Org(
        id=iid(f"{name}_org"),
        name=name,
        owner_id=owner_id,
        group_owner_id=group_owner_id,
        other_read=other_read,
        group_read=group_read,
        member_read=member_read,
    )
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


def create_tour(
    session: Session,
    name: str,
    owner_id: uuid.UUID | None = None,
    group_owner_id: uuid.UUID | None = None,
    other_read: bool = False,
    group_read: bool = False,
    member_read: bool = False,
) -> Tour:
    tour = Tour(
        id=iid(f"{name}_tour"),
        name=name,
        owner_id=owner_id,
        group_owner_id=group_owner_id,
        other_read=other_read,
        group_read=group_read,
        member_read=member_read,
    )
    session.add(tour)
    session.commit()
    session.refresh(tour)
    return tour


def create_event(
    session: Session,
    name: str,
    tour_id: uuid.UUID,
    owner_id: uuid.UUID | None = None,
    group_owner_id: uuid.UUID | None = None,
    other_read: bool = False,
    group_read: bool = False,
    member_read: bool = False,
) -> Event:
    event = Event(
        id=iid(f"{name}_event"),
        tour_id=tour_id,
        owner_id=owner_id,
        group_owner_id=group_owner_id,
        other_read=other_read,
        group_read=group_read,
        member_read=member_read,
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def create_user(
    session: Session, name: str, is_member: bool = False
) -> tuple[User, Org]:
    user = User(
        id=iid(name),
        email=f"{name}@module",
        hashed_password="",
        is_member=is_member,
    )
    session.add(user)
    session.commit()

    org = create_org(session=session, name=name)
    person = create_person(session=session, name=name)

    user.person_id = person.id
    person.owner_id = user.id
    person.group_owner_id = org.id
    org.owner_id = user.id
    org.group_owner_id = org.id

    session.commit()
    session.refresh(user)
    session.refresh(org)
    return user, org


def create_default_users(session: Session) -> tuple[User, Org]:
    superuser = User(email="superuser@module", hashed_password="", is_superuser=True)
    session.add(superuser)
    session.commit()

    session.info["user"] = superuser

    create_user(session, "unprivileged")
    create_user(session=session, name="member", is_member=True)
    owner, owner_org = create_user(session, "owner")

    group_member, group_member_org = create_user(session=session, name="group_member")
    group_member.person.membership_assocs.append(OrgActorAssoc(org=owner_org))
    session.commit()
    return owner, owner_org


@pytest.fixture(scope="function")
def session_no_permission_data(session_function: Session):
    session = session_function
    owner, owner_org = create_default_users(session)

    tour = create_tour(
        session=session,
        name="tour_no_permission",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )
    create_event(
        session=session,
        name="event_no_permission",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )
    create_org(
        session=session,
        name="org_no_permission",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )
    return session


def test_no_permission_unprivileged(session_no_permission_data: Session):
    session = session_no_permission_data
    session.info["user"] = get_user_by_email(
        session=session, email="unprivileged@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_no_permission_group_member(session_no_permission_data: Session):
    session = session_no_permission_data
    session.info["user"] = get_user_by_email(
        session=session, email="group_member@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_no_permission_member(session_no_permission_data: Session):
    session = session_no_permission_data
    session.info["user"] = get_user_by_email(session=session, email="member@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_no_permission_owner(session_no_permission_data: Session):
    session = session_no_permission_data
    session.info["user"] = get_user_by_email(session=session, email="owner@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_no_permission_superuser(session_no_permission_data: Session):
    session = session_no_permission_data
    session.info["user"] = get_user_by_email(session=session, email="superuser@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.fixture(scope="function")
def session_other_read_data(session_function: Session):
    session = session_function
    owner, owner_org = create_default_users(session)

    tour = create_tour(
        session=session,
        name="tour_other_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )
    create_event(
        session=session,
        name="event_other_read",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )
    create_org(
        session=session,
        name="org_other_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )
    return session


def test_other_read_unprivileged(session_other_read_data: Session):
    session = session_other_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="unprivileged@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_other_read_group_member(session_other_read_data: Session):
    session = session_other_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="group_member@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_other_read_member(session_other_read_data: Session):
    session = session_other_read_data
    session.info["user"] = get_user_by_email(session=session, email="member@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_other_read_owner(session_other_read_data: Session):
    session = session_other_read_data
    session.info["user"] = get_user_by_email(session=session, email="owner@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_other_read_superuser(session_other_read_data: Session):
    session = session_other_read_data
    session.info["user"] = get_user_by_email(session=session, email="superuser@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.fixture(scope="function")
def session_member_read_data(session_function: Session):
    session = session_function
    owner, owner_org = create_default_users(session)

    tour = create_tour(
        session=session,
        name="tour_member_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )
    create_event(
        session=session,
        name="event_member_read",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )
    create_org(
        session=session,
        name="org_member_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )
    return session


def test_member_read_unprivileged(session_member_read_data: Session):
    session = session_member_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="unprivileged@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_member_read_group_member(session_member_read_data: Session):
    session = session_member_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="group_member@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_member_read_member(session_member_read_data: Session):
    session = session_member_read_data
    session.info["user"] = get_user_by_email(session=session, email="member@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_member_read_owner(session_member_read_data: Session):
    session = session_member_read_data
    session.info["user"] = get_user_by_email(session=session, email="owner@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_member_read_superuser(session_member_read_data: Session):
    session = session_member_read_data
    session.info["user"] = get_user_by_email(session=session, email="superuser@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 5


@pytest.fixture(scope="function")
def session_group_read_data(session_function: Session):
    session = session_function
    owner, owner_org = create_default_users(session)

    tour = create_tour(
        session=session,
        name="tour_group_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
    create_event(
        session=session,
        name="event_group_ead",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
    create_org(
        session=session,
        name="org_group_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
    return session


def test_group_read_unprivileged(session_group_read_data: Session):
    session = session_group_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="unprivileged@module"
    )

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_group_read_group_member(session_group_read_data: Session):
    session = session_group_read_data
    session.info["user"] = get_user_by_email(
        session=session, email="group_member@module"
    )
    session.info["user"].group_ids = [
        m.org_id for m in session.info["user"].person.membership_assocs
    ]

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_group_read_member(session_group_read_data: Session):
    session = session_group_read_data
    session.info["user"] = get_user_by_email(session=session, email="member@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 0

    events = session.scalars(select(Event)).all()
    assert len(events) == 0

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 1


def test_group_read_owner(session_group_read_data: Session):
    session = session_group_read_data
    session.info["user"] = get_user_by_email(session=session, email="owner@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 2


def test_group_read_superuser(session_group_read_data: Session):
    session = session_group_read_data
    session.info["user"] = get_user_by_email(session=session, email="superuser@module")

    tours = session.scalars(select(Tour)).all()
    assert len(tours) == 1

    events = session.scalars(select(Event)).all()
    assert len(events) == 1

    orgs = session.scalars(select(Org)).all()
    assert len(orgs) == 5
