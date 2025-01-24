import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings
from app.core.db.models import (
    User,
)
from app.core.db.session import SessionDep
from app.core.email.utils import generate_new_account_email, send_email
from app.core.schemas import (
    ErrorResponse,
    PagedResponse,
    PageParamsDep,
)
from app.core.security import (
    CurrentUserDep,
    get_current_active_superuser,
)
from app.users import crud
from app.users.schemas import (
    UserCreate,
    UserPublic,
    UserRegister,
    UserUpdate,
)
from app.utils.schemas import Message

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=PagedResponse[UserPublic],
)
def read(
    session: SessionDep,
    page_params: PageParamsDep,
) -> PagedResponse[UserPublic]:
    """
    Read users.
    """
    users, count = crud.read_users(
        session=session,
        page_params=page_params,
    )
    return PagedResponse[UserPublic].model_validate(
        {
            "total": count,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": users,
        }
    )


@router.get(
    "/me",
    response_model=UserPublic,
)
def read_user_me(current_user: CurrentUserDep) -> User:
    """
    Get current user.
    """
    if current_user is None:
        raise HTTPException(404, "User not found")
    return current_user


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def create(*, session: SessionDep, user_in: UserCreate) -> UserPublic:
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà",
        )

    user = crud.create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return UserPublic.model_validate(user)


@router.post("/signup", response_model=UserPublic)
def register(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Un utilisateur avec cet email existe déjà",
        )
    user_create = UserCreate.model_validate(user_in)
    user = crud.create_user(session=session, user_create=user_create)
    return user


@router.get(
    "/{user_id}",
    response_model=UserPublic,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
def read_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Permissions insuffisantes",
        )
    if not user:
        raise HTTPException(status_code=404, detail="L'utilisateur n'existe pas")
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
def update(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="L'utilisateur que vous essayez de modifier n'existe pas",
        )
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="Un utilisateur avec cet email existe déjà"
            )

    return crud.update_user(session=session, db_user=db_user, user_in=user_in)


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete(
    session: SessionDep, current_user: CurrentUserDep, user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403,
            detail="Les admins ne sont pas autorisés à se supprimer eux-même",
        )
    session.delete(user)
    session.commit()
    return Message(message="Utilisateur supprimé")
