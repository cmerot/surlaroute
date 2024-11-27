import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.core.schemas import LtreeField


class ActivityCreate(BaseModel):
    path: LtreeField
    name: str | None = None


class ActivityUpdate(BaseModel):
    name: str | None = None
    dest_path: LtreeField | None = Field(default=None, min_length=1)


class ActivityPublic(BaseModel):
    id: uuid.UUID
    name: str
    path: LtreeField

    model_config = ConfigDict(from_attributes=True)
