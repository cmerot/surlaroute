import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList

from app.directory.models import (
    Activity,
    Actor,
    AssociationOrgActor,
    Org,
    Person,
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
    mitchum_id = get_fixture_uuid("mitchum")
    armodo_id = get_fixture_uuid("armodo")
    slowfest_id = get_fixture_uuid("slowfest")

    robert = session.get_one(Person, robert_id)
    mitchum = session.get_one(Person, mitchum_id)
    armodo = session.get_one(Org, armodo_id)
    slowfest = session.get_one(Org, slowfest_id)
    om1 = session.get_one(AssociationOrgActor, (armodo_id, robert_id))
    om2 = session.get_one(AssociationOrgActor, (armodo_id, slowfest_id))
    om3 = session.get_one(AssociationOrgActor, (slowfest_id, mitchum_id))

    print_actor(robert)
    assert robert.membership_assocs[0].org is armodo
    assert robert.membership_assocs[0] is om1

    print_actor(mitchum)
    assert mitchum.membership_assocs[0].org is slowfest
    assert mitchum.membership_assocs[0] is om3

    print_actor(armodo)
    assert armodo.member_assocs[0].actor is robert
    assert armodo.member_assocs[0] is om1
    assert armodo.member_assocs[1].actor is slowfest
    assert armodo.member_assocs[1] is om2

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
    p1 = Person(id=p1_id, name="p1")
    p2 = Person(id=p2_id, name="p2")
    om1 = AssociationOrgActor(org=o1, actor=p1)
    om2 = AssociationOrgActor(org=o1, actor=p2)
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
        session.get_one(AssociationOrgActor, (o1_id, p1_id))

    session.rollback()


def test_directory_delete_actor(session: Session) -> None:
    o1_id = get_fixture_uuid("o1")
    p1_id = get_fixture_uuid("p1")
    p2_id = get_fixture_uuid("p2")
    o1 = Org(id=o1_id, name="o1")
    p1 = Person(id=p1_id, name="p1")
    p2 = Person(id=p2_id, name="p2")
    om1 = AssociationOrgActor(org=o1, actor=p1)
    om2 = AssociationOrgActor(org=o1, actor=p2)
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


# def test_my(session: Session):
#     o1 = Org(name="o")
#     p1 = Person(name="p")
#     oa = AssociationOrgActor(org=o1, actor=p1)
#     # o1.members.append()
#     session.add_all([oa])
#     session.commit()


def test_association_org_activity() -> None:
    assert isinstance(Org().activities, InstrumentedList)
    assert isinstance(Activity(name="a").orgs, InstrumentedList)


def test_association_org_actor() -> None:
    assert isinstance(Org().member_assocs, InstrumentedList)
    assert isinstance(Org().membership_assocs, InstrumentedList)
    assert isinstance(Actor().membership_assocs, InstrumentedList)
    assert hasattr(Actor(), "members") is False
    assert isinstance(Person().membership_assocs, InstrumentedList)
    assert hasattr(Person(), "members") is False
    pass


def test_activity_init() -> None:
    activity = Activity(name="a")
    assert activity.name == "a"
    assert str(activity.path) == "a"


def test_activity_init_without_name() -> None:
    with pytest.raises(TypeError):
        Activity(name="a")


def test_activity_init_with_parent_path() -> None:
    activity = Activity(name="b", parent_path="a")
    assert activity.name == "b"
    assert str(activity.path) == "a.b"


def test_activity_init_with_deep_parent_path() -> None:
    activity = Activity(name="c", parent_path="a.b")
    assert activity.name == "c"
    assert str(activity.path) == "a.b.c"


def test_activity_change_name() -> None:
    activity = Activity(name="a")
    assert str(activity.path) == "a"
    activity.name = "a2"
    assert str(activity.path) == "a2"


def test_activity_change_name_with_parent_path() -> None:
    activity = Activity(name="b", parent_path="a")
    assert str(activity.path) == "a.b"
    activity.name = "b2"
    assert str(activity.path) == "a.b2"


def test_activity_change_name_with_deep_parent_path() -> None:
    activity = Activity(name="c", parent_path="a.b")
    activity.name = "c2"
    assert activity.name == "c2"
    assert str(activity.path) == "a.b.c2"
