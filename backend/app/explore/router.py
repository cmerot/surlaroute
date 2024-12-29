from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter
from sqlalchemy import func, select
from sqlalchemy.orm import (
    Session,
    aliased,
    with_polymorphic,
)

from app.core.db.models import (
    Actor,
    Org,
    Person,
    filter_out_actor_assocs,
    get_permission_filter,
)
from app.core.db.session import SessionDep
from app.core.schemas import (
    PagedResponse,
    PageParams,
    PageParamsDep,
)
from app.core.security import CurrentUserOrNoneDep
from app.explore.schemas import Org_Explore, Person_Explore

# from app.core.security import CurrentPermissionsUserDep

router = APIRouter()


# person_membership_assocs = (
#     selectinload(Person.membership_assocs)
#     .selectinload(OrgActorAssoc.org)
#     .options(
#         selectinload(Actor.owner),
#         selectinload(Actor.contact).selectinload(Contact.address),
#         selectinload(Org.activities),
#         org_member_assocs,
#     )
# )

# actor_owner = selectinload(Actor.owner).options(selectinload(User.person))
# actor_address = selectinload(Actor.contact).selectinload(Contact.address)

org_alias = aliased(Org)
person_alias = aliased(Person)


def read_actors(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Actor], int]:
    actor_poly = with_polymorphic(Actor, [Org, Person])

    statement = (
        select(actor_poly)
        # .where(Actor.id == "84b5112b-e1b6-49f7-998d-805e937da1cd")
        .order_by(actor_poly.Org.name)
        .order_by(actor_poly.Person.name)
        .where(actor_poly.type == "Person")
    )
    # actors = session.scalars(statement).unique().all()
    # for actor in actors:
    #     print(actor)
    #     if isinstance(actor, Org):
    #         # print(actor.activities)
    #         pass

    # Add pagination
    paged_statement = statement.offset(page_params.offset).limit(page_params.limit)

    # Retrieve entities
    actors = session.scalars(paged_statement).unique().all()

    # Filter empty associations
    # An association can be empty if the user has not enough permission
    for actor in actors:
        actor.membership_assocs = filter_out_actor_assocs(actor.membership_assocs)

        if isinstance(actor, Org):
            actor.member_assocs = filter_out_actor_assocs(actor.member_assocs)

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


@router.get(
    "/",
    response_model=PagedResponse[Org_Explore | Person_Explore],
    # response_model_exclude_none=True,
)
def get_actors(
    session: SessionDep,
    page_params: PageParamsDep,
    _user: CurrentUserOrNoneDep,
) -> Any:
    """
    Paginated list of actors

    """
    actors, count = read_actors(
        session=session,
        page_params=page_params,
    )
    return {
        "total": count,
        "limit": page_params.limit,
        "offset": page_params.offset,
        "results": actors,
    }
