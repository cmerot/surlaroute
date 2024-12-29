import uuid
from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import (
    Session,
)

from app.core.db.models import (
    Org,
    Tour,
    filter_out_actor_assocs,
    get_permission_filter,
)
from app.core.schemas import PageParams


def get_tour_details(
    *,
    session: Session,
    tour_id: uuid.UUID | None = None,
) -> Tour:
    # select_org_member_assocs = (
    #     selectinload(Org.member_assocs)
    #     .selectinload(OrgActorAssoc.actor)
    #     .selectinload(Actor.contact)
    #     .selectinload(Contact.address)
    # )
    stmt = (
        select(Tour).where(Tour.id == tour_id)
        # .options(
        #     raiseload("*"),
        #     selectinload(Tour.owner).options(selectinload(User.person)),
        #     selectinload(Tour.disciplines),
        #     selectinload(Tour.mobilities),
        #     selectinload(Tour.actor_assocs).options(
        #         selectinload(TourActorAssoc.actor)
        #         .selectinload(Actor.contact)
        #         .selectinload(Contact.address),
        #         selectinload(TourActorAssoc.actor.of_type(Org)).options(
        #             selectinload(Org.member_assocs)
        #             .selectinload(OrgActorAssoc.actor)
        #             .selectinload(Actor.contact)
        #             .selectinload(Contact.address),
        #             selectinload(Org.activities),
        #             selectinload(Org.owner).selectinload(User.person),
        #         ),
        #     ),
        #     selectinload(Tour.events).options(
        #         selectinload(Event.owner).options(selectinload(User.person)),
        #         selectinload(Event.actor_assocs).options(
        #             selectinload(EventActorAssoc.actor).options(
        #                 selectinload(Actor.owner).selectinload(User.person),
        #                 selectinload(Actor.contact).selectinload(Contact.address),
        #             ),
        #             selectinload(EventActorAssoc.actor.of_type(Org)).options(
        #                 selectinload(Org.owner).selectinload(User.person),
        #                 selectinload(Org.activities),
        #                 selectinload(Org.member_assocs)
        #                 .selectinload(OrgActorAssoc.actor)
        #                 .selectinload(Actor.contact)
        #                 .selectinload(Contact.address),
        #             ),
        #         ),
        #     ),
        # )
    )

    tour = session.scalars(stmt).unique().one()

    tour.actor_assocs = filter_out_actor_assocs(tour.actor_assocs)

    for assoc in tour.actor_assocs:
        assoc.actor.membership_assocs = filter_out_actor_assocs(
            assoc.actor.membership_assocs
        )

    for event in tour.events:
        event.actor_assocs = filter_out_actor_assocs(event.actor_assocs)

    return tour


def get_tours(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Tour], int]:
    statement = select(Tour).options(
        # raiseload("*"),
        # selectinload(Tour.owner).options(selectinload(User.person)),
        # selectinload(Tour.events),
        # selectinload(Tour.disciplines),
        # selectinload(Tour.mobilities),
    )

    if page_params.q:
        statement = statement.where(
            or_(
                Tour.name.ilike(f"%{page_params.q}%"),
                Tour.description.ilike(f"%{page_params.q}%"),
            )
        )

    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)
    tours = session.scalars(paged_statement).unique().all()

    new_assocs = []
    for tour in tours:
        for assoc in tour.actor_assocs:
            if assoc.actor:
                new_assocs.append(assoc)
        tour.actor_assocs = new_assocs

    for tour in tours:
        for assoc in tour.actor_assocs:
            assoc.actor.membership_assocs = filter_out_actor_assocs(
                assoc.actor.membership_assocs
            )
            if isinstance(assoc.actor, Org):
                assoc.actor.member_assocs = filter_out_actor_assocs(
                    assoc.actor.member_assocs
                )
        for event in tour.events:
            for assoc in event.actor_assocs:
                assoc.actor.membership_assocs = filter_out_actor_assocs(
                    assoc.actor.membership_assocs
                )
                if isinstance(assoc.actor, Org):
                    assoc.actor.member_assocs = filter_out_actor_assocs(
                        assoc.actor.member_assocs
                    )

    # return [], 0
    # assoc.actor.membership_assocs = filter_out_actor_assocs(
    #     assoc.actor.membership_assocs
    # )

    # for assoc in tour.actor_assocs:
    #     assoc.actor.membership_assocs = filter_out_actor_assocs(
    #         assoc.actor.membership_assocs
    #     )

    # The main statement will be updated on Session.do_orm_execute
    # with permission filters, but it's not yet the case
    # now when we want to count the result.
    # We create a new statement, manually apply filters
    # and count.
    statement = select(Tour.id).filter(
        get_permission_filter(Tour, session.info["user"])
    )
    count_statement = select(func.count()).select_from(statement)

    count = session.scalar(count_statement)

    return tours, count
