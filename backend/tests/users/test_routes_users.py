import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db.models import User
from app.core.security import verify_password
from app.users import crud
from app.users.schemas import UserCreate
from tests.utils import random_email, random_lower_string


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    with (
        patch("app.core.email.utils.send_email", return_value=None),
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        r = client.post(
            "/users/",
            headers=superuser_token_headers,
            json=data,
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.get_user_by_email(session=session, email=username)
        assert user
        assert user.email == created_user["email"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    user_id = user.id
    r = client.get(
        f"/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_current_user(client: TestClient, session: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password, is_active=True)
    user = crud.create_user(session=session, user_create=user_in)
    user_id = user.id

    login_data = {
        "username": username,
        "password": password,
    }
    r = client.post("/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"/users/{user_id}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_existing_user_permissions_error(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.get(
        f"/users/{uuid.uuid4()}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "L'utilisateur n'a pas les permissions suffisantes"}


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.create_user(session=session, user_create=user_in)
    data = {"email": username, "password": password}
    r = client.post(
        "/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        "/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_read_users(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.create_user(session=session, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.create_user(session=session, user_create=user_in2)

    r = client.get("/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users["results"]) > 1
    assert "total" in all_users
    for item in all_users["results"]:
        assert "email" in item


def test_register_user(client: TestClient, session: Session) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        "/users/signup",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == username

    user_query = select(User).where(User.email == username)
    user_db = session.scalar(user_query)
    assert user_db
    assert user_db.email == username
    assert verify_password(password, user_db.hashed_password)


def test_register_user_already_exists_error(client: TestClient) -> None:
    password = random_lower_string()
    data = {
        "email": settings.FIRST_SUPERUSER,
        "password": password,
    }
    r = client.post(
        "/users/signup",
        json=data,
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Un utilisateur avec cet email existe déjà"


def test_update_user(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)

    data = {"is_member": True}
    r = client.patch(
        f"/users/{user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()

    assert updated_user["is_member"] is True

    user_query = select(User).where(User.email == username)
    user_db = session.scalar(user_query)
    session.refresh(user_db)
    assert user_db
    assert user_db.is_member is True


def test_update_user_not_exists(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"full_name": "Updated_full_name"}
    r = client.patch(
        f"/users/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert (
        r.json()["detail"] == "L'utilisateur que vous essayez de modifier n'existe pas"
    )


def test_update_user_email_exists(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    user2 = crud.create_user(session=session, user_create=user_in2)

    data = {"email": user2.email}
    r = client.patch(
        f"/users/{user.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "Un utilisateur avec cet email existe déjà"


def test_delete_user_super_user(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    user_id = user.id
    r = client.delete(
        f"/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    deleted_user = r.json()
    assert deleted_user["message"] == "Utilisateur supprimé"
    result = session.scalar(select(User).where(User.id == user_id))
    assert result is None


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"/users/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"


def test_delete_user_current_super_user_error(
    client: TestClient, superuser_token_headers: dict[str, str], session: Session
) -> None:
    super_user = crud.get_user_by_email(session=session, email=settings.FIRST_SUPERUSER)
    assert super_user
    user_id = super_user.id

    r = client.delete(
        f"/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 403
    assert (
        r.json()["detail"] == "Les admins ne sont pas autorisés à se supprimer eux-même"
    )


def test_delete_user_without_privileges(
    client: TestClient, normal_user_token_headers: dict[str, str], session: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)

    r = client.delete(
        f"/users/{user.id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "The user doesn't have enough privileges"
