from typing import Annotated, Any, Generic, TypeVar

from fastapi import Depends
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.directory.crud_schemas import OrgPublic
from app.users.schemas import UserPublic

T = TypeVar("T")


class PageParams(BaseModel):
    """Request query params for paginated API."""

    q: str | None = Field(default=None)
    limit: int = Field(default=100, gt=0, le=100)
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


class PermissionsPublic(BaseModel):
    owner: UserPublic | None
    owner_group: OrgPublic | None
    group_read: bool = Field(default=True)
    group_write: bool = Field(default=True)
    member_read: bool = Field(default=True)
    member_write: bool = Field(default=False)
    other_read: bool = Field(default=False)
