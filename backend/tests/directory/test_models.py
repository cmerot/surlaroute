import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList

from app.core.db.models import (
    Activity,
    Actor,
    Org,
    OrgActorAssoc,
    Person,
    User,
)
from tests.directory.fixtures import get_fixture_uuid


def print_actor(actor: Actor) -> None:
    print(f"{actor}:")
    if len(actor.membership_assocs) > 0:
        print("  - memberships:")
        for om in actor.membership_assocs:
            print(f"    - {om.org!r}")
    if isinstance(actor, Org) and actor.member_assocs:
        print("  - members:")
        for om in actor.member_assocs:
            print(f"    - {om.actor!r}")


def test_directory_preloaded_fixtures(session: Session) -> None:
    robert_id = get_fixture_uuid("robert")
    eddie_id = get_fixture_uuid("eddie")
    armodo_id = get_fixture_uuid("armodo")
    slowfest_id = get_fixture_uuid("slowfest")

    robert = session.get_one(Person, robert_id)
    mitchum = session.get_one(Person, eddie_id)
    armodo = session.get_one(Org, armodo_id)
    slowfest = session.get_one(Org, slowfest_id)
    om1 = session.get_one(OrgActorAssoc, (armodo_id, robert_id))
    om2 = session.get_one(OrgActorAssoc, (armodo_id, slowfest_id))
    om3 = session.get_one(OrgActorAssoc, (slowfest_id, eddie_id))

    print_actor(robert)
    assert robert.membership_assocs[0].org is armodo
    assert robert.membership_assocs[0] is om1
    assert robert.__class__ is Person

    print_actor(mitchum)
    assert mitchum.membership_assocs[0].org is slowfest
    assert mitchum.membership_assocs[0] is om3

    print_actor(armodo)
    assert armodo.member_assocs[0].actor is robert
    assert armodo.member_assocs[0] is om1
    assert armodo.member_assocs[1].actor is slowfest
    assert armodo.member_assocs[1] is om2
    assert armodo.__class__ is Org

    print_actor(slowfest)
    assert slowfest.membership_assocs[0].org is armodo
    assert slowfest.membership_assocs[0] is om2
    assert slowfest.member_assocs[0].actor is mitchum
    assert slowfest.member_assocs[0] is om3


def test_directory_delete_om(session: Session) -> None:
    o1_id = get_fixture_uuid("o1")
    p1_id = get_fixture_uuid("p1")
    p2_id = get_fixture_uuid("p2")
    o1 = Org(id=o1_id, name="o1")
    p1 = Person(id=p1_id, name="p 1")
    p2 = Person(id=p2_id, name="p 2")
    om1 = OrgActorAssoc(org=o1, actor=p1)
    om2 = OrgActorAssoc(org=o1, actor=p2)
    session.add_all([o1, p1, p2, om1, om2])
    session.flush()

    print_actor(o1)
    assert len(o1.member_assocs) == 2

    session.delete(om1)
    session.flush()

    session.refresh(o1)
    print_actor(o1)
    assert len(o1.member_assocs) == 1

    with pytest.raises(NoResultFound):
        session.get_one(OrgActorAssoc, (o1_id, p1_id))

    session.rollback()


def test_directory_delete_actor(session: Session) -> None:
    o1_id = get_fixture_uuid("o1")
    p1_id = get_fixture_uuid("p1")
    p2_id = get_fixture_uuid("p2")
    o1 = Org(id=o1_id, name="o1")
    p1 = Person(id=p1_id, name="p 1")
    p2 = Person(id=p2_id, name="p 2")
    om1 = OrgActorAssoc(org=o1, actor=p1)
    om2 = OrgActorAssoc(org=o1, actor=p2)
    session.add_all([o1, p1, p2, om1, om2])
    session.flush()

    print_actor(o1)
    assert len(o1.member_assocs) == 2

    session.delete(p2)
    session.flush()

    session.refresh(o1)
    print_actor(o1)
    assert len(o1.member_assocs) == 1

    with pytest.raises(NoResultFound):
        session.get_one(Person, p2_id)

    session.rollback()


def test_association_org_activity() -> None:
    assert isinstance(Org().activities, InstrumentedList)
    assert isinstance(Activity(path="a").orgs, InstrumentedList)


def test_association_org_actor() -> None:
    assert isinstance(Org().member_assocs, InstrumentedList)
    assert isinstance(Org().membership_assocs, InstrumentedList)
    assert isinstance(Actor().membership_assocs, InstrumentedList)
    assert hasattr(Actor(), "members") is False
    assert isinstance(Person().membership_assocs, InstrumentedList)
    assert hasattr(Person(), "members") is False


def test_person_user(session: Session) -> None:
    u = User(email="test_person_user@example.com", hashed_password="nopass")
    p = Person(name="robert")
    p.user = u
    session.add(p)
    session.commit()
    session.refresh(p)
    assert p.user.email == "test_person_user@example.com"


def test_user_person(session: Session) -> None:
    u = User(email="test_user_person@example.com", hashed_password="nopass")
    p = Person(name="robert")
    u.person = p
    session.add(u)
    session.commit()
    session.refresh(u)
    assert u.person.name == "robert"
