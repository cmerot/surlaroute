# Activity
import uuid
from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    PlainSerializer,
    PlainValidator,
    WithJsonSchema,
)
from sqlalchemy_utils import Ltree

LtreeField = Annotated[
    Ltree,
    PlainValidator(lambda o: Ltree(o)),
    PlainSerializer(lambda o: o.path, return_type=str),
    WithJsonSchema({"type": "string", "examples": ["some.path"]}),
]


class ActivityBase(BaseModel):
    name: str | None = Field(default=None)


class ActivityCreate(ActivityBase):
    name: str
    parent_path: str | None = Field(default=None)


class ActivityUpdate(ActivityBase):
    # id: uuid.UUID
    name: str | None = Field(default=None)


class ActivityMove(BaseModel):
    source: LtreeField
    dest: LtreeField | None = Field(default=None)


class ActivityMoveResponse(BaseModel):
    lca: LtreeField | None
    rowcount: int


class ActivityPublic(ActivityBase):
    id: uuid.UUID
    name: str
    path: LtreeField


class ActivitiesPublic(BaseModel):
    data: list[ActivityPublic]
