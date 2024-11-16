import uuid

from pydantic import BaseModel, ConfigDict, Field


class OrganisationPublic(BaseModel):
    id: uuid.UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class OrganisationCreate(BaseModel):
    name: str


class OrganisationUpdate(BaseModel):
    name: str | None = Field(default=None)
