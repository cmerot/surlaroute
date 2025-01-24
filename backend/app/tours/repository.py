from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import (
    Session,
    noload,
    selectinload,
)

from app.core.db.models import (
    Actor,
    Org,
    Tour,
    TourActorAssoc,
)
from app.core.security import get_permission_filter, get_security_context
from app.tours.schemas import ToursPageParams


def get_all_tours(
    *,
    session: Session,
    page_params: ToursPageParams = ToursPageParams(),
) -> tuple[Sequence[Tour], int]:
    """
    Returns all actors paginated and filtered by name or activity
    Will load actors with their memberships and members. Memberships and members' actors
    won't have their own children loaded.
    """

    select_actor = (
        selectinload(TourActorAssoc.actor).options(
            noload(Actor.membership_assocs),
            noload(Actor.tour_assocs),
            noload(Actor.event_assocs),
            noload(Actor.contact),
        ),
        selectinload(TourActorAssoc.actor.of_type(Org)).options(
            noload(Org.member_assocs),
        ),
    )
    statement = select(Tour).options(
        selectinload(Tour.actor_assocs).options(
            *select_actor,
        ),
    )

    # Add pagination
    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)

    # Retrieve entities
    tours = session.scalars(paged_statement).unique().all()

    # Count statement
    # Since the security filter works by inspecting selected columns
    # we need to apply directly the filter
    statement = statement.filter(
        get_permission_filter(Tour, get_security_context(session))
    )
    count_statement = select(func.count()).select_from(statement.subquery())
    count = session.scalars(count_statement).one()

    return tours, count


def get_tour(*, session: Session, id) -> Tour:
    """
    Returns details of tour:
    - tour itself
    - producers (actors with role "producer")
    - list of events
    """

    select_tour_actor = (
        selectinload(TourActorAssoc.actor).options(
            noload(Actor.membership_assocs),
            noload(Actor.tour_assocs),
            noload(Actor.event_assocs),
            noload(Actor.contact),
        ),
        selectinload(TourActorAssoc.actor.of_type(Org)).options(
            noload(Org.member_assocs),
        ),
    )

    # select_event_actor = (
    #     selectinload(EventActorAssoc.actor).options(
    #         noload(Actor.membership_assocs),
    #         noload(Actor.tour_assocs),
    #         noload(Actor.event_assocs),
    #         noload(Actor.contact),
    #     ),
    #     selectinload(EventActorAssoc.actor.of_type(Org)).options(
    #         noload(Org.member_assocs),
    #     ),
    # )

    # select_event = (
    #     selectinload(Event.actor_assocs).options(
    #         *select_event_actor,
    #     ),
    # )

    statement = (
        select(Tour)
        .options(
            selectinload(Tour.actor_assocs).options(
                *select_tour_actor,
            ),
            selectinload(Tour.events).options(
                # select_event,
            ),
        )
        .where(Tour.id == id)
    )

    return session.scalars(statement).one()
