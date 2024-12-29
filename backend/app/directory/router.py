import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.core.schemas import (
    PagedResponse,
    PageParamsDep,
)
from app.core.security import CurrentUserOrNoneDep

# from app.core.security import CurrentPermissionsUserDep
from app.directory import repository
from app.explore.schemas import (
    OrgFull_Explore,
    PersonFull_Explore,
)

router = APIRouter()


@router.get(
    "/",
    response_model=PagedResponse[PersonFull_Explore | OrgFull_Explore],
    response_model_exclude_none=True,
)
def get_actors(
    session: SessionDep,
    page_params: PageParamsDep,
    _user: CurrentUserOrNoneDep,
) -> Any:
    """
    Paginated list of actors

    """
    orgs, count = repository.get_actors(
        session=session,
        page_params=page_params,
    )
    return {
        "total": count,
        "limit": page_params.limit,
        "offset": page_params.offset,
        "results": orgs,
    }


@router.get(
    "/orgs/{id}",
    response_model=OrgFull_Explore,
    response_model_exclude_none=True,
)
def get_org_details(
    session: SessionDep,
    id: uuid.UUID,
    _user: CurrentUserOrNoneDep,
) -> OrgFull_Explore:
    """
    Org details

    """

    try:
        org = repository.get_org_details(
            session=session,
            org_id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Org '{id}' not found",
        )
    return OrgFull_Explore.model_validate(org)


@router.get(
    "/people/{id}",
    response_model=PersonFull_Explore,
    response_model_exclude_none=True,
)
def get_person_details(
    session: SessionDep,
    id: uuid.UUID,
    _user: CurrentUserOrNoneDep,
) -> PersonFull_Explore:
    """
    Person details

    """

    try:
        person = repository.get_person_details(
            session=session,
            person_id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Person '{id}' not found",
        )

    return PersonFull_Explore.model_validate(person)
