from typing import Annotated, Generic, TypeVar

from fastapi import Depends
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    PlainValidator,
    WithJsonSchema,
)
from sqlalchemy_utils import Ltree

T = TypeVar("T")


class PageParams(BaseModel):
    """Request query params for paginated API."""

    q: str | None = Field(default=None)
    limit: int = Field(default=100, gt=0, le=100)
    offset: int = Field(default=0, ge=0)


# PageParamsDep = Annotated[dict, Depends(PageParams)]
PageParamsDep = Annotated[PageParams, Depends()]

LtreeField = Annotated[
    str | Ltree,
    PlainValidator(lambda o: Ltree(o)),
    PlainSerializer(lambda o: o.path, return_type=str),
    WithJsonSchema({"type": "string", "examples": ["some.path"]}),
]


class PagedResponse(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    limit: int
    offset: int
    results: list[T]


class UpdateResponse(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    success: bool
    data: T | None = None
    message: str | None = None

    model_config = ConfigDict(from_attributes=True)


class DeleteResponse(BaseModel):
    """Response schema for any paged API."""

    success: bool
    message: str | None = None

    model_config = ConfigDict(from_attributes=True)
