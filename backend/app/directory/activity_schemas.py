# Activity
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.directory.schemas import LtreeField


class ActivityCreate(BaseModel):
    name: str
    parent_path: LtreeField | None = Field(default=None)


class ActivityUpdate(BaseModel):
    name: str | None = Field(default=None)
    parent_path: LtreeField | None = Field(default=None)


class ActivityUpdateResponse(BaseModel):
    lca: LtreeField | None
    rowcount: int


class ActivityDeleteResponse(BaseModel):
    rowcount: int


class ActivityPublic(BaseModel):
    id: uuid.UUID
    name: str
    path: LtreeField

    model_config = ConfigDict(from_attributes=True)


class ActivitiesPublic(BaseModel):
    data: list[ActivityPublic]

    model_config = ConfigDict(from_attributes=True)
