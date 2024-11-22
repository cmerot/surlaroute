import uuid

from pydantic import BaseModel, ConfigDict, Field


class OrgPublic(BaseModel):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrgCreate(BaseModel):
    name: str


class OrgUpdate(BaseModel):
    name: str | None = Field(default=None)
