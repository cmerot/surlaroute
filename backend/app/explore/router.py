from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from geoalchemy2 import WKBElement
from geoalchemy2.functions import ST_Intersects, ST_MakeEnvelope
from geoalchemy2.shape import to_shape
from geojson_pydantic import MultiLineString, Point
from shapely.geometry import Point as ShapelyPoint
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import Ltree

from app.activities.schemas import TreePublic
from app.core.db.models import (
    Event,
    EventActorAssoc,
    Mobility,
    Org,
    Person,
    Tour,
    TourActorAssoc,
)
from app.core.db.session import SessionDep
from app.core.schemas import (
    AddressPublic,
    PageParams,
)
from app.core.security import CurrentUserOrNoneDep
from app.explore.schemas import (
    ActorFeature,
    EventPointFeature,
    EventPointFeatureProperties,
    OrgFeatureProperties,
    OrgGeo,
    PersonFeatureProperties,
    PersonGeo,
    TourFeatureCollection,
    TourFeatureCollectionProperties,
    TourLineFeature,
    TourLineFeatureProperties,
)

router = APIRouter()


class ExplorePageParams(PageParams):
    activity: str | None = None
    bbox: str
    mobility_path: str | None = None


ExplorePageParamsDep = Annotated[ExplorePageParams, Depends()]


# def get_orgs(
#     page_params: ExplorePageParamsDep,
#     session: Session,
# ) -> FeatureCollection[Feature[Point, OrgFeatureProperties]]:
#     """Get all orgs that have a geom_point"""
#     statement = (
#         select(Org)
#         .join(Org.contact)
#         .join(Contact.address)
#         .where(AddressGeo.geom_point.isnot(None))
#     )

#     if page_params.q is not None and page_params.q != "":
#         statement = statement.where(
#             or_(
#                 Org.name.ilike(f"%{page_params.q}%"),
#                 Org.description.ilike(f"%{page_params.q}%"),
#             )
#         )

#     if page_params.activity is not None and page_params.activity != "":
#         statement = statement.join(Org.activities).filter(
#             Activity.path.descendant_of(Ltree(page_params.activity))
#         )

#     orgs = session.scalars(statement).all()
#     features = []
#     for org in orgs:
#         address = AddressPublic.model_validate(org.contact.address)
#         feature: ActorFeature[OrgFeatureProperties] = ActorFeature(
#             type="Feature",
#             properties=OrgFeatureProperties(
#                 id=org.id,
#                 name=org.name,
#                 type="org",
#                 description=org.description,
#                 activities=[
#                     TreePublic.model_validate(activity) for activity in org.activities
#                 ],
#             ),
#             geometry=Point(
#                 type="Point",  # Required
#                 coordinates=address.geom_point.coordinates,
#             ),
#         )

#         features.append(feature)

#     return FeatureCollection(
#         type="FeatureCollection",
#         features=features,
#     )


def get_tour_feature_geomety(tour: Tour) -> MultiLineString | None:
    """Return a multiline geometry joining all tour events location"""

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
        return None
    return MultiLineString(type="MultiLineString", coordinates=[coordinates])


def get_center_coordinates_of_wkbelement_list(
    points: list[WKBElement],
) -> tuple[float, float]:
    # Convert WKB to shapely points
    shapely_points = [to_shape(p) for p in points]

    # Calculate average coordinates
    x_avg = sum(p.x for p in shapely_points) / len(shapely_points)
    y_avg = sum(p.y for p in shapely_points) / len(shapely_points)

    # Create new Point and return as tuple
    point = ShapelyPoint(x_avg, y_avg)
    return (point.x, point.y)


def get_event_feature_geometry(event: Event) -> Point | None:
    """Return a Point geometry in the center of all event's actors with role diffusion"""

    coordinates = []
    for actor in event.event_venues:
        if actor.contact.address.geom_point:
            coordinates.append(actor.contact.address.geom_point)

    if len(coordinates) < 1:
        return None

    return Point(
        type="Point", coordinates=get_center_coordinates_of_wkbelement_list(coordinates)
    )


# Query functions
def get_tours_in_bbox(
    session: Session,
    mobility_path: str | None,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> Sequence[Tour]:
    """Get all tours that intersect with the given bounding box"""
    # Create the query
    statement = (
        select(Tour)
        .filter(
            ST_Intersects(
                Tour.bbox,
                ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326),
            )
        )
        .order_by(Tour.year.desc())  # type: ignore[attr-defined]
    )

    if mobility_path is not None and mobility_path != "":
        statement = statement.join(Tour.mobilities).filter(
            Mobility.path.descendant_of(Ltree(mobility_path))
        )

    # Execute the query
    return session.scalars(statement).all()


def get_tour_feature_collection(tour: Tour) -> TourFeatureCollection:
    features: list[TourLineFeature | EventPointFeature | ActorFeature] = []
    tour.events.sort(key=lambda e: e.start_dt if e.start_dt is not None else -1)

    # Tour feature:
    # - the multiline that represents all events
    # - some meta info about the tour
    feature = TourLineFeature(
        type="Feature",
        geometry=get_tour_feature_geomety(tour),
        properties=TourLineFeatureProperties(
            id=tour.id,
            type="tour_line",
        ),
    )
    features.append(feature)
    features.extend(get_actor_assoc_features(tour.actor_assocs, "tour_actor", tour.id))

    # For each event, an Event feature:
    # - the point that represents the event
    # - some meta info about the event
    for event in tour.events:
        event_feature = EventPointFeature(
            type="Feature",
            geometry=get_event_feature_geometry(event),
            properties=EventPointFeatureProperties(
                id=event.id,
                type="event_point",
                name=event.name,
                start_dt=event.start_dt,
                end_dt=event.end_dt,
                tour_id=tour.id,
                event_venues=[
                    OrgGeo.model_validate(v)
                    if v.type == "Org"
                    else PersonGeo.model_validate(v)
                    for v in event.event_venues
                ],
            ),
        )
        features.append(event_feature)
        features.extend(
            get_actor_assoc_features(tour.actor_assocs, "event_actor", event.id)
        )

    return TourFeatureCollection(
        type="FeatureCollection",
        features=features,
        properties=TourFeatureCollectionProperties(
            id=tour.id,
            type="tour_collection",
            name=tour.name,
            description=tour.description,
            year=tour.year,
            producers=[
                OrgGeo.model_validate(p)
                if p.type == "Org"
                else PersonGeo.model_validate(p)
                for p in tour.producers
            ],
            disciplines=[
                TreePublic.model_validate(discipline) for discipline in tour.disciplines
            ],
            mobilities=[
                TreePublic.model_validate(mobility) for mobility in tour.mobilities
            ],
        ),
    )


def get_actor_assoc_features(
    actor_assocs: list[TourActorAssoc] | list[EventActorAssoc],
    type: Literal["tour_actor", "event_actor"],
    parent_id: uuid.UUID,
) -> list[ActorFeature[OrgFeatureProperties | PersonFeatureProperties]]:
    features = []
    for assoc in actor_assocs:
        if (
            assoc.actor.contact is None
            or assoc.actor.contact.address.geom_point is None
        ):
            continue

        properties: OrgFeatureProperties | PersonFeatureProperties

        if isinstance(assoc.actor, Org):
            properties = OrgFeatureProperties(
                id=assoc.actor.id,
                type=type,
                parent_id=parent_id,
                name=assoc.actor.name,
                role=assoc.data.get("role"),
                description=assoc.actor.description,
                activities=[
                    TreePublic.model_validate(activity)
                    for activity in assoc.actor.activities
                ],
            )
        elif isinstance(assoc.actor, Person):
            properties = PersonFeatureProperties(
                id=assoc.actor.id,
                type=type,
                parent_id=parent_id,
                name=assoc.actor.name,
                role=assoc.data.get("role"),
            )
        else:
            raise ValueError(f"Unknown actor type: {assoc.actor.__class__.__name__}")

        geometry = Point(
            type="Point",
            coordinates=get_center_coordinates_of_wkbelement_list(
                [assoc.actor.contact.address.geom_point]  # type: ignore[list-item]
            ),
        )
        feature: ActorFeature[
            OrgFeatureProperties | PersonFeatureProperties
        ] = ActorFeature(
            type="Feature",
            id=str(assoc.actor.id),
            geometry=geometry,
            properties=properties,
        )
        features.append(feature)
    return features


@router.get(
    "/",
    response_model=list[TourFeatureCollection],
    response_model_exclude_none=True,
)
def get_data(
    session: SessionDep,
    page_params: ExplorePageParamsDep,
    user: CurrentUserOrNoneDep,
) -> list[TourFeatureCollection]:
    session.info["user"] = user

    # Get tours in the bounding box
    tours = get_tours_in_bbox(
        session,
        page_params.mobility_path,
        *map(float, page_params.bbox.split(",")),
    )

    # List of collections to return
    results: list[TourFeatureCollection] = []

    for tour in tours:
        results.append(get_tour_feature_collection(tour))

    return results
