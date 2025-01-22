from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated, Generic, Literal

from geojson_pydantic import MultiLineString, Point
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypeVar

from app.activities.schemas import TreePublic

# Base models


class OrgGeo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    type: Literal["Org"]
    name: str
    activities: list[TreePublic]


class PersonGeo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    type: Literal["Person"]
    name: str


ActorGeo = Annotated[OrgGeo | PersonGeo, Field(discriminator="type")]

# GeoJSON Features

## GeoJSON Actor Features (Org and Person)


class ActorFeatureProperties(BaseModel):
    id: uuid.UUID
    type: Literal["tour_actor", "event_actor"]
    parent_id: uuid.UUID
    name: str
    role: str | None = None


class OrgFeatureProperties(ActorFeatureProperties):
    id: uuid.UUID
    actor_type: Literal["Org"] = "Org"
    description: str | None = None
    activities: list[TreePublic]


class PersonFeatureProperties(ActorFeatureProperties):
    actor_type: Literal["Person"] = "Person"


Props = TypeVar("Props", bound=OrgFeatureProperties | PersonFeatureProperties)


class ActorFeature(BaseModel, Generic[Props]):
    type: Literal["Feature"]
    geometry: Point
    properties: Props


## GeoJSON Event Feature


class EventPointFeature(BaseModel):
    type: Literal["Feature"]
    geometry: Point
    properties: EventPointFeatureProperties


class EventPointFeatureProperties(BaseModel):
    id: uuid.UUID
    type: Literal["event_point"]
    # name: str
    start_dt: datetime
    end_dt: datetime | None = None
    tour_id: uuid.UUID
    event_venues: list[ActorGeo]


## GeoJSON Tour Feature


class TourLineFeature(BaseModel):
    type: Literal["Feature"]
    geometry: MultiLineString
    properties: TourLineFeatureProperties


class TourLineFeatureProperties(BaseModel):
    id: uuid.UUID
    type: Literal["tour_line"]


## GeoJSON Tour Feature Collection


class TourFeatureCollection(BaseModel):
    """
    GeoJSON description of a tour. One TourLineFeature and multiple EventPointFeature.

    Features:
    - EventPointFeature: an event's venue as a point
    - TourLineFeature: a multiline joining event venues

    Properties:
    - some metadata about the tour: description, year, producers, disciplines, mobilities
    - an ActorAssocFeatureCollection: show a tour's actors
    - a list of ActorAssocFeatureCollection: show each event's actors
    """

    type: Literal["FeatureCollection"]
    features: list[TourLineFeature | EventPointFeature | ActorFeature]
    properties: TourFeatureCollectionProperties


class TourFeatureCollectionProperties(BaseModel):
    """
    Properties of a TourFeatureCollection.
    """

    id: uuid.UUID
    type: Literal["tour_collection"]
    name: str
    description: str | None = None
    year: int
    producers: list[ActorGeo]
    disciplines: list[TreePublic]
    mobilities: list[TreePublic]
