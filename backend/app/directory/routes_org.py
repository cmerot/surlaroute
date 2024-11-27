import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.core.schemas import (
    DeleteResponse,
    PagedResponse,
    PageParamsDep,
    UpdateResponse,
)
from app.core.security import CurrentPermissionsUserDep
from app.directory import crud
from app.directory.crud_schemas import (
    OrgCreate,
    OrgPublic,
    OrgUpdate,
)

router = APIRouter()


@router.post("/", response_model=OrgPublic)
def create_org(
    *,
    session: SessionDep,
    user: CurrentPermissionsUserDep,
    org_create: OrgCreate,
) -> Any:
    """Create an org."""
    print(f"user -> {user}")
    print(f"user.person -> {user.person}")
    org = crud.create_org(
        session=session,
        entity_in=org_create,
    )
    return OrgPublic.model_validate(org)


@router.get("/{id}", response_model=OrgPublic)
def read_org_by_id(
    session: SessionDep,
    id: uuid.UUID,
) -> OrgPublic:
    """Read an org by its id."""

    try:
        org = crud.read_org(
            session=session,
            id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Org '{id}' not found",
        )
    return OrgPublic.model_validate(org)


@router.get("/", response_model=PagedResponse[OrgPublic])
def read_orgs(
    session: SessionDep,
    page_params: PageParamsDep,
) -> PagedResponse[OrgPublic]:
    """Read paginated orgs."""

    orgs, count = crud.read_orgs(
        session=session,
        page_params=page_params,
    )
    return PagedResponse[OrgPublic].model_validate(
        {
            "total": count,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": orgs,
        }
    )


@router.patch("/{id}", response_model=UpdateResponse[OrgPublic])
def update_org(
    *,
    session: SessionDep,
    id: uuid.UUID,
    org_update: OrgUpdate,
) -> UpdateResponse[OrgPublic]:
    """Update an org."""

    try:
        org = crud.update_org(
            session=session,
            id=id,
            org_update=org_update,
        )
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Org not found",
        )

    return UpdateResponse[OrgPublic].model_validate(
        {
            "success": True,
            "data": org,
        }
    )


@router.delete("/{id}", response_model=DeleteResponse)
def delete_org(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> DeleteResponse:
    """Delete an org."""

    try:
        crud.delete_org(session=session, id=id)
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Org not found",
        )

    return DeleteResponse.model_validate(
        {
            "success": True,
            "message": f"Org {id} deleted",
        }
    )
