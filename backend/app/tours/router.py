from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from geojson_pydantic import FeatureCollection
from sqlalchemy.exc import NoResultFound

from app.core.db.models import Tour
from app.core.db.session import SessionDep
from app.core.schemas import AddressPublic, ErrorResponse, PagedResponse, TourPublic
from app.core.security import OAuthSecurityContextDep
from app.tours import repository
from app.tours.schemas import (
    ToursPageParamsDep,
)

router = APIRouter()


def get_tour_feature_collection(tour: Tour) -> FeatureCollection:
    """Return a GeoJSON FeatureCollection representing the tour"""
    tour.events.sort(key=lambda e: e.start_dt if e.start_dt is not None else -1)

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
        return FeatureCollection.model_validate(
            {
                "type": "FeatureCollection",
                "features": [],
            }
        )

    return FeatureCollection.model_validate(
        {
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
    )


@router.get(
    "/",
    response_model=PagedResponse[TourPublic],
    response_model_exclude_none=True,
    dependencies=[OAuthSecurityContextDep],
)
def get_all_tours(
    session: SessionDep,
    page_params: ToursPageParamsDep,
) -> Any:
    """
    Paginated list of tours

    """

    actors, count = repository.get_all_tours(session=session, page_params=page_params)

    return {
        "total": count,
        "limit": page_params.limit,
        "offset": page_params.offset,
        "results": actors,
    }


@router.get(
    "/tours/{id}",
    response_model=TourPublic,
    response_model_exclude_none=True,
    responses={
        404: {"model": ErrorResponse},
    },
    dependencies=[OAuthSecurityContextDep],
)
def get_tour(
    session: SessionDep,
    id: uuid.UUID,
) -> Tour:
    """
    Tour details
    """

    try:
        tour = repository.get_tour(session=session, id=id)
        # TODO: serialize geojson in TourPublic
        tour.geojson = get_tour_feature_collection(tour)  # type: ignore
        return tour
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f"Tour '{id}' non trouvé",
        )
