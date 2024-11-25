import uuid

from pydantic import BaseModel, ConfigDict, Field


class PersonPublic(BaseModel):
    id: uuid.UUID
    firstname: str
    lastname: str

    model_config = ConfigDict(from_attributes=True)


class PersonCreate(BaseModel):
    firstname: str
    lastname: str


class PersonUpdate(BaseModel):
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
