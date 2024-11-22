import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList

from app.directory.models import (
    Activity,
    Actor,
    AssociationOrganisationActor,
    Organisation,
    Person,
)
from tests.directory.fixtures import get_fixture_uuid


def print_actor(actor: Actor) -> None:
    print(f"{actor}:")
    if len(actor.memberships) > 0:
        print("  - memberships:")
        for om in actor.memberships:
            print(f"    - {om.organisation!r}")
    if isinstance(actor, Organisation) and actor.members:
        print("  - members:")
        for om in actor.members:
            print(f"    - {om.actor!r}")


def test_directory_preloaded_fixtures(session: Session) -> None:
    robert_id = get_fixture_uuid("robert")
    mitchum_id = get_fixture_uuid("mitchum")
    armodo_id = get_fixture_uuid("armodo")
    slowfest_id = get_fixture_uuid("slowfest")

    robert = session.get_one(Person, robert_id)
    mitchum = session.get_one(Person, mitchum_id)
    armodo = session.get_one(Organisation, armodo_id)
    slowfest = session.get_one(Organisation, slowfest_id)
    om1 = session.get_one(AssociationOrganisationActor, (armodo_id, robert_id))
    om2 = session.get_one(AssociationOrganisationActor, (armodo_id, slowfest_id))
    om3 = session.get_one(AssociationOrganisationActor, (slowfest_id, mitchum_id))

    print_actor(robert)
    assert robert.memberships[0].organisation is armodo
    assert robert.memberships[0] is om1

    print_actor(mitchum)
    assert mitchum.memberships[0].organisation is slowfest
    assert mitchum.memberships[0] is om3

    print_actor(armodo)
    assert armodo.members[0].actor is robert
    assert armodo.members[0] is om1
    assert armodo.members[1].actor is slowfest
    assert armodo.members[1] is om2

    print_actor(slowfest)
    assert slowfest.memberships[0].organisation is armodo
    assert slowfest.memberships[0] is om2
    assert slowfest.members[0].actor is mitchum
    assert slowfest.members[0] is om3


def test_directory_delete_om(session: Session) -> None:
    o1_id = get_fixture_uuid("o1")
    p1_id = get_fixture_uuid("p1")
    p2_id = get_fixture_uuid("p2")
    o1 = Organisation(id=o1_id, name="o1")
    p1 = Person(id=p1_id, name="p1")
    p2 = Person(id=p2_id, name="p2")
    om1 = AssociationOrganisationActor(organisation=o1, actor=p1)
    om2 = AssociationOrganisationActor(organisation=o1, actor=p2)
    session.add_all([o1, p1, p2, om1, om2])
    session.flush()

    print_actor(o1)
    assert len(o1.members) == 2

    session.delete(om1)
    session.flush()

    session.refresh(o1)
    print_actor(o1)
    assert len(o1.members) == 1

    with pytest.raises(NoResultFound):
        session.get_one(AssociationOrganisationActor, (o1_id, p1_id))

    session.rollback()


def test_directory_delete_actor(session: Session) -> None:
    o1_id = get_fixture_uuid("o1")
    p1_id = get_fixture_uuid("p1")
    p2_id = get_fixture_uuid("p2")
    o1 = Organisation(id=o1_id, name="o1")
    p1 = Person(id=p1_id, name="p1")
    p2 = Person(id=p2_id, name="p2")
    om1 = AssociationOrganisationActor(organisation=o1, actor=p1)
    om2 = AssociationOrganisationActor(organisation=o1, actor=p2)
    session.add_all([o1, p1, p2, om1, om2])
    session.flush()

    print_actor(o1)
    assert len(o1.members) == 2

    session.delete(p2)
    session.flush()

    session.refresh(o1)
    print_actor(o1)
    assert len(o1.members) == 1

    with pytest.raises(NoResultFound):
        session.get_one(Person, p2_id)

    session.rollback()


# def test_my(session: Session):
#     o1 = Organisation(name="o")
#     p1 = Person(name="p")
#     oa = AssociationOrganisationActor(organisation=o1, actor=p1)
#     # o1.members.append()
#     session.add_all([oa])
#     session.commit()


def test_association_organisation_activity() -> None:
    assert isinstance(Organisation().activities, InstrumentedList)
    assert isinstance(Activity(name="a").organisations, InstrumentedList)


def test_association_organisation_actor() -> None:
    assert isinstance(Organisation().members, InstrumentedList)
    assert isinstance(Organisation().memberships, InstrumentedList)
    assert isinstance(Actor().memberships, InstrumentedList)
    assert hasattr(Actor(), "members") is False
    assert isinstance(Person().memberships, InstrumentedList)
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
