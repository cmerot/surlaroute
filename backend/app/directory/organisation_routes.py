import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.directory import organisation_crud as crud
from app.directory.organisation_schemas import (
    OrganisationCreate,
    OrganisationPublic,
    OrganisationUpdate,
)
from app.directory.schemas import (
    DeleteResponse,
    PagedResponse,
    PageParamsDep,
    UpdateResponse,
)

router = APIRouter()


@router.post("/", response_model=OrganisationPublic)
def create_organisation(
    *,
    session: SessionDep,
    organisation_create: OrganisationCreate,
) -> Any:
    """Create an organisation."""

    org = crud.create_organisation(
        session=session,
        organisation_create=organisation_create,
    )
    return OrganisationPublic.model_validate(org)


@router.get("/{id}", response_model=OrganisationPublic)
def read_organisation_by_id(
    session: SessionDep,
    id: uuid.UUID,
) -> OrganisationPublic:
    """Read an organisation by its id."""

    try:
        org = crud.read_organisation(
            session=session,
            id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Organisation '{id}' not found",
        )
    return OrganisationPublic.model_validate(org)


@router.get("/", response_model=PagedResponse[OrganisationPublic])
def read_organisations(
    session: SessionDep,
    page_params: PageParamsDep,
) -> PagedResponse[OrganisationPublic]:
    """Read paginated organisations."""

    orgs, count = crud.read_organisations(
        session=session,
        page_params=page_params,
    )
    return PagedResponse[OrganisationPublic].model_validate(
        {
            "total": count,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": orgs,
        }
    )


@router.patch("/{id}", response_model=UpdateResponse[OrganisationPublic])
def update_organisation(
    *,
    session: SessionDep,
    id: uuid.UUID,
    organisation_update: OrganisationUpdate,
) -> UpdateResponse[OrganisationPublic]:
    """Update an organisation."""

    try:
        org = crud.update_organisation(
            session=session,
            id=id,
            organisation_update=organisation_update,
        )
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Organisation not found",
        )

    return UpdateResponse[OrganisationPublic].model_validate(
        {
            "success": True,
            "data": org,
        }
    )


@router.delete("/{id}", response_model=DeleteResponse)
def delete_organisation(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> DeleteResponse:
    """Delete an organisation."""

    try:
        crud.delete_organisation(session=session, id=id)
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Organisation not found",
        )

    return DeleteResponse.model_validate(
        {
            "success": True,
            "message": f"Organisation {id} deleted",
        }
    )
