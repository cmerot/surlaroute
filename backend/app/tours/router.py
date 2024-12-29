import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from geojson_pydantic import FeatureCollection
from sqlalchemy.exc import NoResultFound

from app.core.db.session import SessionDep
from app.core.schemas import (
    AddressPublic,
    PagedResponse,
    PageParamsDep,
)
from app.core.security import CurrentUserOrNoneDep
from app.tours import repository
from app.tours.schemas import (
    TourPublic,
)

router = APIRouter()


@router.get(
    "/tours/{id}.geojson",
    response_model=FeatureCollection,
    response_model_exclude_none=True,
)
def get_tour_details_geojson(
    session: SessionDep,
    id: uuid.UUID,
    _user: CurrentUserOrNoneDep,
) -> Any:
    """
    Tour geojson at /tours/tours/{id}.geojson

    """

    try:
        tour = repository.get_tour_details(session=session, tour_id=id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Tour '{id}' non trouvé",
        )

    tour.events.sort(key=lambda e: e.start_dt)
    # Generate a MultiLineString, each LineString representing the way between two events
    coordinates = []
    for i in range(len(tour.events) - 1):
        event1 = tour.events[i]
        event2 = tour.events[i + 1]

        address1 = AddressPublic.model_validate(
            event1.actor_assocs[0].actor.contact.address
        )
        address2 = AddressPublic.model_validate(
            event2.actor_assocs[0].actor.contact.address
        )
        if address1.geom_point and address2.geom_point:
            coordinates.append(address1.geom_point.coordinates)
            coordinates.append(address2.geom_point.coordinates)

    if len(coordinates) < 1:
        return {
            "type": "FeatureCollection",
            "features": [],
        }

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [coordinates],
                },
                "properties": {"name": tour.name},
            }
        ],
    }


@router.get(
    "/tours/{id}",
    response_model=TourPublic,
    response_model_exclude_none=True,
)
def get_tour_details(
    session: SessionDep,
    id: uuid.UUID,
    _user: CurrentUserOrNoneDep,
) -> Any:
    # ) -> Tour:
    """
    Tour details at /tours/tours/{id}

    """

    try:
        tour = repository.get_tour_details(session=session, tour_id=id)
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Tour '{id}' non trouvé",
        )
    return tour


@router.get(
    "/",
    response_model=PagedResponse[TourPublic],
    response_model_exclude_none=True,
)
def get_tours(
    session: SessionDep,
    page_params: PageParamsDep,
    _user: CurrentUserOrNoneDep,
) -> Any:
    """
    Tours list at /

    """

    tours, count = repository.get_tours(session=session, page_params=page_params)
    return {
        "total": count,
        "limit": page_params.limit,
        "offset": page_params.offset,
        "results": tours,
    }
