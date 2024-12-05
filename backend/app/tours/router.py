import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.core.schemas import (
    PagedResponse,
    PageParamsDep,
)
from app.directory.crud_schemas import (
    TourPublic,
)

# from app.core.security import CurrentPermissionsUserDep
from app.tours import crud

router = APIRouter()


@router.get("/{id}", response_model=TourPublic)
def read_tour_by_id(
    session: SessionDep,
    id: uuid.UUID,
) -> TourPublic:
    """Read an tour by its id."""

    try:
        tour = crud.read_tour(
            session=session,
            id=id,
        )
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Tour '{id}' not found",
        )
    return TourPublic.model_validate(tour)


@router.get("/", response_model=PagedResponse[TourPublic])
def read_tours(
    session: SessionDep,
    page_params: PageParamsDep,
) -> PagedResponse[TourPublic]:
    """Read paginated tours."""

    tours, count = crud.read_tours(
        session=session,
        page_params=page_params,
    )
    return PagedResponse[TourPublic].model_validate(
        {
            "total": count,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": tours,
        }
    )
