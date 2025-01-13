from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import (
    Session,
    noload,
    selectinload,
    with_polymorphic,
)
from sqlalchemy_utils import Ltree

from app.core.db.models import (
    Activity,
    Actor,
    Event,
    EventActorAssoc,
    Org,
    OrgActorAssoc,
    Person,
    Tour,
    TourActorAssoc,
    get_permission_filter,
)
from app.directory.schemas import DirectoryPageParams


def get_all_actors(
    *,
    session: Session,
    page_params: DirectoryPageParams = DirectoryPageParams(),
) -> tuple[Sequence[Actor], int]:
    """
    Returns all actors paginated and filtered by name or activity
    Will load actors with their memberships and members. Memberships and members' actors
    won't have their own children loaded.
    """

    actor_poly = with_polymorphic(Actor, [Org, Person])

    select_org = selectinload(OrgActorAssoc.org).options(
        noload(Org.member_assocs),
        noload(Org.membership_assocs),
        noload(Org.contact),
    )

    select_actor = (
        selectinload(OrgActorAssoc.actor).options(
            noload(Actor.membership_assocs),
            noload(Actor.contact),
        ),
        selectinload(OrgActorAssoc.actor.of_type(Org)).options(
            noload(Org.member_assocs)
        ),
    )
    statement = select(actor_poly).options(
        selectinload(actor_poly.membership_assocs).options(
            *select_actor,
            select_org,
        ),
        selectinload(actor_poly.contact),
        selectinload(actor_poly.Org.member_assocs).options(
            *select_actor,
            select_org,
        ),
        noload(actor_poly.tour_assocs),
    )

    if page_params.q is not None and page_params.q != "":
        statement = statement.where(
            or_(
                actor_poly.Org.name.ilike(f"%{page_params.q}%"),
                actor_poly.Org.description.ilike(f"%{page_params.q}%"),
                actor_poly.Person.name.ilike(f"%{page_params.q}%"),
            )
        )
    if page_params.activity is not None and page_params.activity != "":
        statement = statement.join(actor_poly.Org.activities).filter(
            Activity.path.descendant_of(Ltree(page_params.activity))
        )

    # Add pagination
    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)

    # Retrieve entities
    actors = session.scalars(paged_statement).unique().all()

    # Count statement
    # Since the security filter works by inspecting selected columns
    # we need to apply directly the filter
    statement = statement.filter(get_permission_filter(Actor, session.info["user"]))
    count_statement = select(func.count()).select_from(statement.subquery())
    count = session.scalars(count_statement).one()

    return actors, count


def get_org(*, session: Session, id) -> Org:
    """
    Returns details of an org:
    - org itself
    - memberships
    - members
    - tours
    """

    select_org = selectinload(OrgActorAssoc.org).options(
        noload(Org.member_assocs),
        noload(Org.membership_assocs),
    )

    select_actor = (
        selectinload(OrgActorAssoc.actor).options(
            noload(Actor.membership_assocs),
        ),
        selectinload(OrgActorAssoc.actor.of_type(Org)).options(
            noload(Org.member_assocs)
        ),
    )

    select_tour = selectinload(TourActorAssoc.tour).options(
        noload(Tour.actor_assocs),
    )
    statement = (
        select(Org)
        .options(
            selectinload(Org.membership_assocs).options(
                *select_actor,
                select_org,
            ),
            selectinload(Org.member_assocs).options(
                *select_actor,
                select_org,
            ),
            selectinload(Org.tour_assocs).options(
                select_tour,
            ),
        )
        .where(Org.id == id)
    )

    return session.scalars(statement).one()


def get_person(*, session: Session, id) -> Person:
    """
    Returns details of a person:
    - person itself
    - memberships
    - tours
    - events
    """

    select_org = selectinload(OrgActorAssoc.org).options(
        noload(Org.member_assocs),
        noload(Org.membership_assocs),
    )

    select_actor = (
        selectinload(OrgActorAssoc.actor).options(
            noload(Actor.membership_assocs),
        ),
        selectinload(OrgActorAssoc.actor.of_type(Org)).options(
            noload(Org.member_assocs)
        ),
    )

    select_tour = selectinload(TourActorAssoc.tour).options(
        noload(Tour.actor_assocs),
        noload(Tour.events),
    )

    select_event = selectinload(EventActorAssoc.event).options(
        noload(Event.actor_assocs),
    )

    statement = (
        select(Person)
        .options(
            selectinload(Person.membership_assocs).options(
                *select_actor,
                select_org,
            ),
            selectinload(Person.tour_assocs).options(
                select_tour,
            ),
            selectinload(Person.event_assocs).options(
                select_event,
            ),
        )
        .where(Person.id == id)
    )

    return session.scalars(statement).one()
