import uuid

from pydantic import BaseModel, ConfigDict, Field


class PersonPublic(BaseModel):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(BaseModel):
    name: str


class PersonUpdate(BaseModel):
    name: str | None = Field(default=None)
