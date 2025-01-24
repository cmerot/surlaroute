from __future__ import annotations

import uuid
from typing import Any, Union

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.models import (
    Org,
    Person,
)
from app.core.db.session import SessionDep
from app.core.schemas import ErrorResponse, OrgPublic, PagedResponse, PersonPublic
from app.core.security import (
    OAuthSecurityContextDep,
)
from app.directory import repository
from app.directory.schemas import (
    DirectoryPageParamsDep,
)

router = APIRouter()


@router.get(
    "/",
    response_model=PagedResponse[Union[OrgPublic, PersonPublic]],  # noqa: UP007
    response_model_exclude_none=True,
    dependencies=[OAuthSecurityContextDep],
)
def get_all_actors(
    session: SessionDep,
    page_params: DirectoryPageParamsDep,
) -> Any:
    """
    Paginated list of actors

    """

    actors, count = repository.get_all_actors(session=session, page_params=page_params)
    print(count)

    return {
        "total": count,
        "limit": page_params.limit,
        "offset": page_params.offset,
        "results": actors,
    }


@router.get(
    "/orgs/{id}",
    response_model=OrgPublic,
    response_model_exclude_none=True,
    responses={
        404: {"model": ErrorResponse},
    },
    dependencies=[OAuthSecurityContextDep],
)
def get_org(
    session: SessionDep,
    id: uuid.UUID,
) -> Org:
    """
    Org details
    """

    try:
        return repository.get_org(session=session, id=id)
    except NoResultFound:
        raise HTTPException(status_code=404)


@router.get(
    "/people/{id}",
    response_model=PersonPublic,
    response_model_exclude_none=True,
    responses={
        404: {"model": ErrorResponse},
    },
    dependencies=[OAuthSecurityContextDep],
)
def get_person(
    session: SessionDep,
    id: uuid.UUID,
) -> Person:
    """
    Person details

    """

    try:
        return repository.get_person(session=session, id=id)
    except NoResultFound:
        raise HTTPException(status_code=404)
