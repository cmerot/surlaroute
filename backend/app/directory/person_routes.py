import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.directory import person_crud as crud
from app.directory.person_schemas import (
    PersonCreate,
    PersonPublic,
    PersonUpdate,
)
from app.directory.schemas import (
    DeleteResponse,
    PagedResponse,
    PageParamsDep,
    UpdateResponse,
)

router = APIRouter()


@router.post("/", response_model=PersonPublic)
def create_person(
    *,
    session: SessionDep,
    person_create: PersonCreate,
) -> Any:
    """Create a person."""

    org = crud.create_person(
        session=session,
        person_create=person_create,
    )
    return PersonPublic.model_validate(org)


@router.get("/{id}", response_model=PersonPublic)
def read_person_by_id(
    session: SessionDep,
    id: uuid.UUID,
) -> PersonPublic:
    """Read a person by its id."""

    try:
        org = crud.read_person(
            session=session,
            id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Person '{id}' not found",
        )
    return PersonPublic.model_validate(org)


@router.get("/", response_model=PagedResponse[PersonPublic])
def read_people(
    session: SessionDep,
    page_params: PageParamsDep,
) -> PagedResponse[PersonPublic]:
    """Read paginated people."""

    orgs, count = crud.read_people(
        session=session,
        page_params=page_params,
    )
    return PagedResponse[PersonPublic].model_validate(
        {
            "total": count,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": orgs,
        }
    )


@router.patch("/{id}", response_model=UpdateResponse[PersonPublic])
def update_person(
    *,
    session: SessionDep,
    id: uuid.UUID,
    person_update: PersonUpdate,
) -> UpdateResponse[PersonPublic]:
    """Update a person."""

    try:
        org = crud.update_person(
            session=session,
            id=id,
            person_update=person_update,
        )
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Person not found",
        )

    return UpdateResponse[PersonPublic].model_validate(
        {
            "success": True,
            "data": org,
        }
    )


@router.delete("/{id}", response_model=DeleteResponse)
def delete_person(
    *,
    session: SessionDep,
    id: uuid.UUID,
) -> DeleteResponse:
    """Delete a person."""

    try:
        crud.delete_person(session=session, id=id)
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(
            status_code=404,
            detail="Person not found",
        )

    return DeleteResponse.model_validate(
        {
            "success": True,
            "message": f"Person {id} deleted",
        }
    )
