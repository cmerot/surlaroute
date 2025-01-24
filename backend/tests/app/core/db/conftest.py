import uuid

import pytest
from sqlalchemy.orm import Session

from app.core.db.models import (
    Event,
    Org,
    OrgActorAssoc,
    Person,
    Tour,
    User,
)
from app.core.security import set_security_context_from_user


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
    session.flush()
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
    session.flush()
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
    session.flush()
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
    session.flush()
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

    org = create_org(session=session, name=name)
    person = create_person(session=session, name=name)
    session.add_all([user, person, org])
    user.person = person
    session.flush()

    person.owner_id = user.id
    person.group_owner_id = org.id
    org.owner_id = user.id
    org.group_owner_id = org.id
    person.membership_assocs.append(OrgActorAssoc(org=org))
    session.flush()

    return user, org


def create_default_users(session: Session) -> tuple[User, Org]:
    """
    Create the following users:

    - superuser: has all permissions (is_superuser=True)
    - unprivileged: just a user
    - member: member user (is_member=True)
    - owner: the owner of the tour, event, and org
    - group_member: a member of the owner's group
    """
    superuser = User(email="superuser@module", hashed_password="", is_superuser=True)
    session.add(superuser)
    session.flush()

    set_security_context_from_user(session, superuser)

    # Unprivileged user
    create_user(session, "unprivileged")

    # Member user
    create_user(session=session, name="member", is_member=True)

    # Owner user
    owner, owner_org = create_user(session, "owner")

    # Group member user, belongs to owner's group
    group_member, _group_member_org = create_user(session=session, name="group_member")
    group_member.person.membership_assocs.append(OrgActorAssoc(org=owner_org))  # type: ignore
    session.flush()

    # Set group ids for the group member, normally done by the security module
    # in the routing via `get_current_user_or_none` and `CurrentUserOrNoneDep`
    group_member.set_group_ids()

    return owner, owner_org


@pytest.fixture(scope="function")
def entities_with_default_permissions(db_session: Session) -> None:
    """
    Create the following entities with default permissions:

    - tour
    - event
    - org
    """
    owner, owner_org = create_default_users(db_session)
    tour = create_tour(
        session=db_session,
        name="tour_default_permissions",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )
    create_event(
        session=db_session,
        name="event_default_permissions",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )
    create_org(
        session=db_session,
        name="org_default_permissions",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
    )


@pytest.fixture(scope="function")
def entities_with_other_read_permission(db_session: Session):
    """
    Create the following entities with other_read=True:

    - tour
    - event
    - org
    """
    owner, owner_org = create_default_users(db_session)

    tour = create_tour(
        session=db_session,
        name="tour_other_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )
    create_event(
        session=db_session,
        name="event_other_read",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )
    create_org(
        session=db_session,
        name="org_other_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        other_read=True,
    )


@pytest.fixture(scope="function")
def entities_with_member_read_permission(db_session: Session):
    """
    Create the following entities with member_read=True:

    - tour
    - event
    - org
    """
    owner, owner_org = create_default_users(db_session)

    tour = create_tour(
        session=db_session,
        name="tour_member_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )
    create_event(
        session=db_session,
        name="event_member_read",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )
    create_org(
        session=db_session,
        name="org_member_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        member_read=True,
    )


@pytest.fixture(scope="function")
def entities_with_group_member_read_permission(db_session: Session):
    owner, owner_org = create_default_users(db_session)

    tour = create_tour(
        session=db_session,
        name="tour_group_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
    create_event(
        session=db_session,
        name="event_group_ead",
        tour_id=tour.id,
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
    create_org(
        session=db_session,
        name="org_group_read",
        owner_id=owner.id,
        group_owner_id=owner_org.id,
        group_read=True,
    )
