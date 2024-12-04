#!/usr/bin/env python
# mypy: ignore-errors
import json

from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from sqlalchemy_utils import Ltree
from tabulate import tabulate

from app.core.db.models import Activity, Org, OrgActivity, Person, Tour
from app.core.db.session import SessionLocal

db = SessionLocal()


if __name__ == "__main__":
    # People
    people = (
        db.query(Person)
        .filter(Person.owner_id == None)  # noqa: E711
        .all()
    )
    rows = [["person", "owner_id"]]
    for p in people:
        if p.user:
            line = [p.name, p.user.email]
            rows.append(line)
            p.owner_id = p.user.id
            db.add(p)
    print(tabulate(rows, headers="firstrow"))
    db.commit()

    # Tours and events
    tours = (
        db.query(Tour)
        .options(joinedload(Tour.actor_assocs))
        .order_by(Tour.name)
        .where(Tour.owner_id == None)  # noqa: E711
        .all()
    )
    rows = [["event", "venue", "tour", "group_owner", "owner"]]
    for t in tours:
        tour_ressources = []
        for a in t.actor_assocs:
            data = json.loads(a.data)["role"]
            if data == "producer":
                tour_ressources.append(a.actor)

        if len(tour_ressources) < 1:
            raise Exception("owner not found")

        group_owner = tour_ressources[0]
        owner = group_owner.member_assocs[0].actor.user
        t.owner_id = owner.id
        t.group_owner_id = group_owner.id
        db.add(t)
        for e in t.events:
            line = []
            line.append(e.start_dt)
            line.append(e.event_venue.name)
            line.append(t.name)
            line.append(group_owner.name)
            line.append(owner.email)
            rows.append(line)
            e.owner_id = owner.id
            e.group_owner_id = group_owner.id
            e.event_venue.owner_id = owner.id
            e.event_venue.group_owner_id = group_owner.id
            db.add(e)
            db.add(e.event_venue)
    print(tabulate(rows, headers="firstrow"))
    db.commit()

    # Ressources
    ressources = (
        db.query(Org)
        .join(OrgActivity)
        .join(Activity)
        .filter(
            and_(
                Activity.path.descendant_of(Ltree("Structure.Ressource")),
                Org.owner_id == None,  # noqa: E711
            )
        )
        .order_by(Activity.path, Org.name)
    )

    rows = [["ressource", "group_owner", "owner"]]
    for o in ressources:
        line = []
        line.append(o.name)

        tour_ressources = []
        for a in o.tour_assocs:
            data = json.loads(a.data)["role"]
            if data == "ressource":
                tour_ressources.append(a.tour)

        if len(tour_ressources) < 1:
            raise Exception("tour not found")

        tour = tour_ressources[0]

        tour_ressources = []
        for a in tour.actor_assocs:
            data = json.loads(a.data)["role"]
            if data == "producer":
                tour_ressources.append(a.actor)

        if len(tour_ressources) < 1:
            raise Exception("owner not found")
        group_owner = tour_ressources[0]
        o.group_owner_id = group_owner.id
        o.owner_id = group_owner.member_assocs[0].actor.user.id
        db.add(o)
        line.append(group_owner.name)
        line.append(group_owner.member_assocs[0].actor.user.email)
        rows.append(line)
    db.commit()
    print(tabulate(rows, headers="firstrow"))

    # Production
    productions = (
        db.query(Org)
        .join(OrgActivity)
        .join(Activity)
        .filter(
            and_(
                Activity.path.descendant_of(Ltree("Structure.Production")),
                Org.owner_id == None,  # noqa: E711
            )
        )
        .order_by(Activity.path, Org.name)
    )

    rows = [["productions", "group_owner", "owner"]]
    for p in productions:
        line = []
        line.append(p.name)
        rows.append(line)
        p.group_owner_id = p.id
        p.owner_id = p.member_assocs[0].actor.user.id
        line.append(p.name)
        line.append(p.member_assocs[0].actor.user.email)
        rows.append(line)
        db.add(p)
    db.commit()
    print(tabulate(rows, headers="firstrow"))
