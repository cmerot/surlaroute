from __future__ import annotations

import uuid
from typing import Annotated, Any, Generic, TypeVar

import geoalchemy2
import geojson_pydantic
import geojson_pydantic.types
from fastapi import Depends
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)
from sqlalchemy_utils import Ltree

T = TypeVar("T")


class PageParams(BaseModel):
    """Request query params for paginated API."""

    q: str | None = Field(default=None)
    limit: int = Field(default=10, gt=0, le=100)
    offset: int = Field(default=0, ge=0)


# PageParamsDep = Annotated[dict, Depends(PageParams)]
PageParamsDep = Annotated[PageParams, Depends()]


class PagedResponse(BaseModel, Generic[T]):
    """Response schema for any paged read request."""

    total: int
    limit: int
    offset: int
    results: list[T]


class UpdateResponse(BaseModel, Generic[T]):
    """Response schema for any update request."""

    success: bool
    data: T | None = None
    message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    """Response schema for any delete request."""

    success: bool
    data: Any | None = None
    message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Base(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        exclude_none=True,
        exclude_unset=True,
    )


class PermissionMixin:
    owner_id: uuid.UUID | None = None
    group_owner_id: uuid.UUID | None = None

    other_read: bool
    member_read: bool
    group_read: bool

    owner: OwnerPublic | None = None


class OwnerPersonPublic(Base):
    id: uuid.UUID
    name: str


class OwnerPublic(Base):
    person: OwnerPersonPublic | None = None


class AddressPublic(Base):
    q: str
    geom_point: geojson_pydantic.Point | None = None

    @field_validator("geom_point", mode="before")
    def serialize_geom_point(
        v: geoalchemy2.WKBElement,
    ) -> geojson_pydantic.Point | None:
        """Plain serializer for GeomPoint"""
        if not v:
            return None

        if not isinstance(v, geoalchemy2.WKBElement):
            raise ValueError("Not a WKBElement")

        shape = geoalchemy2.shape.to_shape(v)

        coords = geojson_pydantic.types.Position2D(
            latitude=shape.coords[0][0], longitude=shape.coords[0][1]
        )
        return geojson_pydantic.Point(type="Point", coordinates=coords)


class ContactPublic(Base):
    email_address: str | None = None
    phone_number: str | None = None
    address: AddressPublic | None = None
    website: str | None = None


class TreePublic(Base):
    name: str
    path: str

    @field_validator("path", mode="before")
    def validate_path(v: Ltree):
        return str(v)
