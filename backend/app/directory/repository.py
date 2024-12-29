import uuid
from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, with_polymorphic

from app.core.db.models import (
    Actor,
    Org,
    Person,
    filter_out_actor_assocs,
    get_permission_filter,
)
from app.core.schemas import PageParams


def get_org_details(
    *,
    session: Session,
    org_id: uuid.UUID | None = None,
) -> Org:
    stmt = (
        select(Org).where(Org.id == org_id)
        # .options(
        #     raiseload("*"),
        #     selectinload(Org.owner).selectinload(User.person),
        #     selectinload(Org.activities),
        #     selectinload(Org.contact).selectinload(Contact.address),
        #     selectinload(Org.member_assocs)
        #     .selectinload(OrgActorAssoc.actor)
        #     .options(
        #         selectinload(Actor.owner).selectinload(User.person),
        #         selectinload(Actor.contact).selectinload(Contact.address),
        #     ),
        #     selectinload(Actor.membership_assocs)
        #     .selectinload(OrgActorAssoc.actor)
        #     .options(
        #         selectinload(Actor.owner).selectinload(User.person),
        #         selectinload(Actor.contact).selectinload(Contact.address),
        #     ),
        # )
    )

    org = session.scalars(stmt).unique().one()

    org.member_assocs = filter_out_actor_assocs(org.member_assocs)
    org.membership_assocs = filter_out_actor_assocs(org.membership_assocs)

    return org


def get_orgs(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Org], int]:
    statement = select(Org).options(
        # raiseload("*"),
        # selectinload(Org.owner).options(selectinload(User.person)),
        # selectinload(Org.contact).selectinload(Contact.address),
        # selectinload(Org.member_assocs)
        # .selectinload(OrgActorAssoc.actor)
        # .options(
        #     selectinload(Actor.contact).selectinload(Contact.address),
        #     selectinload(Actor.owner).selectinload(User.person),
        # ),
        # selectinload(Org.activities),
    )

    if page_params.q:
        statement = statement.where(
            or_(
                Org.name.ilike(f"%{page_params.q}%"),
                Org.description.ilike(f"%{page_params.q}%"),
            )
        )

    # Final request that will be executed
    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)
    orgs = session.scalars(paged_statement).unique().all()
    for org in orgs:
        org.member_assocs = filter_out_actor_assocs(org.member_assocs)
        org.tour_assocs = filter_out_actor_assocs(org.tour_assocs)
        for tour_assoc in org.tour_assocs:
            for event in tour_assoc.tour.events:
                event.actor_assocs = filter_out_actor_assocs(event.actor_assocs)

    # The main statement will be updated on Session.do_orm_execute
    # with permission filters, but it's not yet the case
    # now when we want to count the result.
    # We create a new statement, manually apply filters
    # and count.
    filtered_statement = statement.filter(
        get_permission_filter(Org, session.info["user"])
    )
    count_statement = select(func.count()).select_from(filtered_statement)
    count = session.scalar(count_statement)

    return orgs, count


def get_person_details(
    *,
    session: Session,
    person_id: uuid.UUID | None = None,
) -> Person:
    stmt = (
        select(Person).where(Person.id == person_id)
        # .options(
        #     raiseload("*"),
        #     selectinload(Person.owner).selectinload(User.person),
        #     selectinload(Person.contact).selectinload(Contact.address),
        #     selectinload(Person.membership_assocs).options(
        #         selectinload(OrgActorAssoc.org).options(
        #             selectinload(Org.owner).selectinload(User.person),
        #             selectinload(Org.activities),
        #             selectinload(Org.contact).selectinload(Contact.address),
        #             selectinload(Org.member_assocs)
        #             .selectinload(OrgActorAssoc.actor)
        #             .options(
        #                 selectinload(Actor.contact).selectinload(Contact.address),
        #             ),
        #         )
        #     ),
        # )
    )

    person = session.scalars(stmt).unique().one()

    for assoc in person.membership_assocs:
        assoc.org.member_assocs = filter_out_actor_assocs(assoc.org.member_assocs)

    return person


def get_actors(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Actor], int]:
    actor_poly = with_polymorphic(Actor, [Org, Person])

    statement = (
        select(actor_poly)
        # .where(Actor.id == "84b5112b-e1b6-49f7-998d-805e937da1cd")
        # .order_by(actor_poly.Person.name)
        # .order_by(actor_poly.Org.name)
    )
    if page_params.q:
        print("yo")
        statement = statement.where(
            or_(
                actor_poly.Org.name.ilike(f"%{page_params.q}%"),
                actor_poly.Org.description.ilike(f"%{page_params.q}%"),
                actor_poly.Person.name.ilike(f"%{page_params.q}%"),
            )
        )

    # Add pagination
    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)

    # Retrieve entities
    actors = session.scalars(paged_statement).unique().all()

    for actor in actors:
        print(actor.__class__.__name__)
    # return [], 0

    # Filter empty associations
    # An association can be empty if the user has not enough permission
    for actor in actors:
        actor.membership_assocs = filter_out_actor_assocs(actor.membership_assocs)
        if isinstance(actor, Org):
            actor.member_assocs = filter_out_actor_assocs(actor.member_assocs)
            actor.tour_assocs = filter_out_actor_assocs(actor.tour_assocs)
            for tour_assoc in actor.tour_assocs:
                for event in tour_assoc.tour.events:
                    event.actor_assocs = filter_out_actor_assocs(event.actor_assocs)

    # Count statement
    # The main statement will be updated on Session.do_orm_execute
    # with permission filters, but it's not yet the case
    # now when we want to count the result.
    # We create a new statement, manually apply filters
    # and count.
    filtered_statement = statement.filter(
        get_permission_filter(Actor, session.info["user"])
    )
    count_statement = select(func.count()).select_from(filtered_statement)
    count = session.scalar(count_statement)

    return actors, count
