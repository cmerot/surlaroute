from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import Column, ColumnElement, Select, and_, or_, select, true
from sqlalchemy.event import listens_for
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload, raiseload, selectinload
from sqlalchemy.orm.query import QueryContext
from sqlalchemy.orm.session import ORMExecuteState
from sqlalchemy.sql.elements import BooleanClauseList

from app.core import security
from app.core.config import settings
from app.core.db.models import (
    Actor,
    Base,
    Contact,
    OrgActorAssoc,
    Person,
    RowLevelRestrictionMixin,
    User,
)
from app.core.db.session import SessionDep
from app.users.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

reusable_oauth2_no_auto_error = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token", auto_error=False
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]

NoAutoErrorTokenDep = Annotated[str, Depends(reusable_oauth2_no_auto_error)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


@dataclass
class SecurityContext:
    user_id: uuid.UUID | None = None
    is_superuser: bool = False
    is_member: bool = False
    group_ids: list[uuid.UUID] = field(default_factory=list)


def set_security_context(session: Session, security_context: SecurityContext) -> None:
    session.info["security_context"] = security_context


def get_security_context(session: Session) -> SecurityContext:
    security_context = session.info.get("security_context")
    if security_context is None:
        security_context = SecurityContext()
        set_security_context(session, security_context)
    return security_context


def set_security_context_from_user(session: Session, user: User | None) -> None:
    if user is None:
        return
    security_context = get_security_context(session)
    security_context.user_id = user.id
    security_context.is_superuser = user.is_superuser
    security_context.is_member = user.is_member
    stmt = (
        select(User)
        .where(User.id == user.id)
        .options(
            raiseload("*"),
            joinedload(User.person).options(
                joinedload(Person.membership_assocs).options(
                    selectinload(OrgActorAssoc.org)
                ),
            ),
        )
    )

    # We already know the user exists, so we can ignore the type error
    user = session.scalar(stmt)  # type: ignore
    if user is not None and user.person:
        security_context.group_ids = [m.org_id for m in user.person.membership_assocs]

    session.expunge_all()


def set_security_context_from_oauth(
    session: SessionDep, token: NoAutoErrorTokenDep
) -> None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        return

    try:
        statement = select(User).where(
            and_(
                User.id == token_data.sub,
                User.is_active == True,  # noqa: E712
            )
        )
        user = session.scalars(statement).one()

    except NoResultFound:
        return

    set_security_context_from_user(session, user)


OAuthSecurityContextDep = Depends(set_security_context_from_oauth)


def get_current_active_superuser(current_user: CurrentUserDep) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now(timezone.utc)
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=security.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return str(decoded_token["sub"])
    except InvalidTokenError:
        return None


def get_permission_filter(
    model: type[RowLevelRestrictionMixin], security_context: SecurityContext
) -> BooleanClauseList | ColumnElement[bool]:
    """
    Return a filter for the given model and user.
    """
    if security_context and security_context.is_superuser:
        return true()

    criteria = []

    # Public other_read gives access
    criteria.append(model.other_read == True)  # noqa: E712

    # If no user is logged in, that's it
    if not security_context:
        return or_(*criteria)

    # Ownership: a user can select its own entities
    if security_context.user_id:
        criteria.append(model.owner_id == security_context.user_id)

    # If the user is a member, the entity may be available
    if security_context.is_member:
        criteria.append(model.member_read == True)  # noqa: E712

    # If the user is a member of a group, the entity may be available
    criteria.append(
        and_(
            model.group_read == True,  # noqa: E712
            model.group_owner_id.in_(security_context.group_ids),
        )
    )

    return or_(*criteria)


def get_model_from_table_name(table_name: str) -> type[Base] | None:
    for mapper in Base.registry.mappers:
        if mapper.class_.__tablename__ == table_name:
            return mapper.class_
    return None


@listens_for(Session, "do_orm_execute")
def add_permission_filters_on_select(orm_execute_state: ORMExecuteState) -> None:
    """
    On Session `do_orm_execute` event, add filters on subclasses of PermissionsMixin
    by inspecting the exported_columns of the statement.
    """

    if not isinstance(orm_execute_state.statement, Select):
        return

    security_context = get_security_context(orm_execute_state.session)

    models = set()

    # First pass to build the models set
    for col in orm_execute_state.statement.exported_columns:
        # Could have a func instead of a real col
        if not isinstance(col, Column):
            continue
        model = get_model_from_table_name(col.table.name)
        if model:
            models.add(model)

    # Second pass, add filters
    for model in models:
        if issubclass(model, RowLevelRestrictionMixin) or isinstance(model, Actor):
            orm_execute_state.statement = orm_execute_state.statement.filter(
                get_permission_filter(model, security_context)
            )


@listens_for(Contact, "load")
def remove_fields_on_load(target: Contact, context: QueryContext):
    # remove fields based on the security context and the model's permissions field
    security_context = get_security_context(context.session)

    if security_context.is_superuser:
        return

    for field_name, permissions in target.permissions.items():
        if not permissions["other_read"] and security_context.user_id is None:
            setattr(target, field_name, None)
            continue
        if not permissions["member_read"] and security_context.is_member is None:
            setattr(target, field_name, None)
            continue
