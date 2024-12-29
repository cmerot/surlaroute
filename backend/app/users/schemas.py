# Shared properties
import uuid
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = False
    is_superuser: bool = False
    is_member: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class UserPersonOrg(BaseModel):
    id: uuid.UUID
    name: str


class UserPersonOrgAssoc(BaseModel):
    data: dict[str, Any]
    org: UserPersonOrg


class UserPerson(BaseModel):
    id: uuid.UUID
    name: str
    membership_assocs: list[UserPersonOrgAssoc]


class UserPublic(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    is_member: bool
    person: UserPerson | None = None


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
