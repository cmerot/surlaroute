#!/usr/bin/env python

"""
This script aims to add an owner and owner_group to ressources
created during import:

- tours,
- events,
- persons,
- and organisations.

If a person has a user, then that user is the owner.

The group owner of a tour is the first org attached to a tour via a "producer" relation.
The owner of a tour is the first member of that org.

We use that owner and group to set ownership of:

- tour,
- tour actors,
- tour events,
- tour events actors,
- tour event venue,
- tour event venue actors,
- and each time an actor is an org and has members, then we also set the membership on those members
"""

from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from tabulate import tabulate

from app.core.db.models import (
    Actor,
    Event,
    EventActorAssoc,
    Org,
    OrgActorAssoc,
    Person,
    Tour,
    TourActorAssoc,
    User,
)
from app.core.db.session import SessionLocal

db = SessionLocal()


def find_first_tour_org_producer(tour: Tour) -> Org | None:
    """
    Returns the first org attached to a tour via a "producer" relation.
    """
    for assoc in tour.actor_assocs:
        if isinstance(assoc.actor, Org) and assoc.data["role"] == "producer":
            return assoc.actor
    return None


def find_first_org_person_member(org: Org) -> User | None:
    """
    Returns the first person member which has a user of an org
    """
    for assoc in org.member_assocs:
        if isinstance(assoc.actor, Person) and assoc.actor.user:
            return assoc.actor.user
    return None


def set_actor_ownership(actor: Actor, owner_group: Org, owner: User) -> None:
    # Actor owner
    if isinstance(actor, Org | Person):
        if not actor.owner_id:
            actor.owner_id = owner.id
        if not actor.group_owner_id:
            actor.group_owner_id = owner_group.id

    # Org members owner
    if isinstance(actor, Org):
        set_actor_assocs_ownership(actor.member_assocs, owner_group, owner)


def set_actor_assocs_ownership(
    actor_assocs: list[EventActorAssoc] | list[TourActorAssoc] | list[OrgActorAssoc],
    owner_group: Org,
    owner: User,
) -> None:
    for assoc in actor_assocs:
        set_actor_ownership(assoc.actor, owner_group=owner_group, owner=owner)


def set_tour_events_ownership(tour: Tour, owner_group: Org, owner: User) -> None:
    for event in tour.events:
        # Event owner
        event.owner_id = owner.id
        event.group_owner_id = owner_group.id

        # Event actors owner
        set_actor_assocs_ownership(event.actor_assocs, owner_group, owner)

        # Event venue owner
        set_actor_ownership(event.event_venue, owner_group, owner)


def set_tours_ownership() -> None:
    tours = (
        db.query(Tour)
        .options(joinedload(Tour.actor_assocs))
        .order_by(Tour.name)
        # .where(Tour.owner_id == None)  # noqa: E711
        .all()
    )
    for t in tours:
        tour_owner_group = find_first_tour_org_producer(t)
        if not tour_owner_group:
            raise Exception("tour owner group not found")

        tour_owner = find_first_org_person_member(tour_owner_group)
        if not tour_owner:
            raise Exception("tour owner not found")

        # Tour owner
        t.owner_id = tour_owner.id
        t.group_owner_id = tour_owner_group.id

        # Tour events owner
        set_tour_events_ownership(t, tour_owner_group, tour_owner)

        # Tour actors owner
        set_actor_assocs_ownership(t.actor_assocs, tour_owner_group, tour_owner)


def set_people_with_user_ownership() -> None:
    people = (
        db.query(Person)
        .filter(and_(Person.owner_id == None, Person.user != None))  # noqa: E711
        .all()
    )
    for p in people:
        if p.user:
            p.owner_id = p.user.id


def set_orgs_with_members_ownership() -> None:
    orgs = (
        db.query(Org)
        .filter(Org.owner_id == None)  # noqa: E711
        .all()
    )
    for o in orgs:
        if (
            isinstance(o.member_assocs[0].actor, Person)
            and o.member_assocs[0].actor.user
        ):
            o.group_owner_id = o.id
            o.owner_id = o.member_assocs[0].actor.user.id


def print_entities_without_ownership() -> None:
    lines = [["Type", "Entity", "Extra"]]

    people = (
        db.query(Person)
        .filter(Person.owner_id == None)  # noqa: E711
        .all()
    )
    for p in people:
        lines.append(
            ["Person", p.name, ", ".join([m.org.name for m in p.membership_assocs])]
        )

    orgs = (
        db.query(Org)
        .filter(Org.owner_id == None)  # noqa: E711
        .all()
    )
    for o in orgs:
        lines.append(
            ["Tour", o.name, ", ".join([m.actor.name for m in o.member_assocs])]  # type: ignore[attr-defined]
        )

    tours = (
        db.query(Tour)
        .filter(Tour.owner_id == None)  # noqa: E711
        .all()
    )
    for t in tours:
        lines.append(["Tour", t.name])

    events = (
        db.query(Event)
        .filter(Event.owner_id == None)  # noqa: E711
        .all()
    )
    for e in events:
        lines.append(["Event", e.start_dt.strftime("%Y-%m-%d") if e.start_dt else ""])

    if len(lines) > 1:
        print(tabulate(lines, headers="firstrow"))


if __name__ == "__main__":
    set_people_with_user_ownership()
    set_tours_ownership()
    set_orgs_with_members_ownership()
    db.commit()

    print_entities_without_ownership()
