from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, raiseload, selectinload

from app.core import security
from app.core.config import settings
from app.core.db.models import OrgActorAssoc, Person, User
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


def get_current_user_or_none(
    session: SessionDep, token: NoAutoErrorTokenDep
) -> User | None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        session.info["user"] = None
        return None

    try:
        statement = select(User).where(
            and_(
                User.id == token_data.sub,
                User.is_active == True,  # noqa: E712
            )
        )
        user = session.scalars(statement).one()

    except NoResultFound:
        session.info["user"] = None
        return None

    session.info["user"] = user

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
    user.set_group_ids()

    session.expunge_all()
    return user


CurrentUserOrNoneDep = Annotated[User, Depends(get_current_user_or_none)]


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
