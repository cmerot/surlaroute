from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy_utils import Ltree


class TreePublic(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    name: str
    path: str

    @field_validator("path", mode="before")
    @classmethod
    def validate_path(cls, v: Ltree) -> str:
        return str(v)
