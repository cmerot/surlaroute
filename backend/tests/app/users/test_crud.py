from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.core.db.models import User
from app.core.security import verify_password
from app.users import crud
from app.users.schemas import UserCreate, UserUpdate
from tests.app.utils import random_email, random_lower_string


def test_create_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_active=True)
    user = crud.create_user(session=session, user_create=user_in)
    authenticated_user = crud.authenticate(
        session=session, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.authenticate(session=session, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_active=True)
    user = crud.create_user(session=session, user_create=user_in)
    assert user.is_active is True


def test_check_if_user_is_active_inactive(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    assert user.is_active is False


def test_check_if_user_is_superuser(session: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.create_user(session=session, user_create=user_in)
    assert user.is_superuser is True


def test_check_if_user_is_superuser_normal_user(session: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    assert user.is_superuser is False


def test_get_user(session: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.create_user(session=session, user_create=user_in)
    user_2 = session.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(session: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.create_user(session=session, user_create=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.update_user(session=session, db_user=user, user_in=user_in_update)
    user_2 = session.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
