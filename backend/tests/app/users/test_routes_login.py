from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db.models import User
from app.core.security import generate_password_reset_token, verify_password


@pytest.mark.usefixtures("function_create_superuser")
def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.usefixtures("function_create_superuser")
def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = client.post("/login/access-token", data=login_data)
    assert r.status_code == 400


@pytest.mark.usefixtures("function_create_normaluser")
def test_use_access_token(
    client: TestClient, normaluser_token_headers: dict[str, str]
) -> None:
    r = client.post(
        "/login/test-token",
        headers=normaluser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


@pytest.mark.usefixtures("function_create_normaluser")
def test_recovery_password(
    client: TestClient, normaluser_token_headers: dict[str, str]
) -> None:
    with (
        patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
        patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        email = settings.EMAIL_TEST_USER
        r = client.post(f"/password-recovery/{email}", headers=normaluser_token_headers)
        assert r.status_code == 200
        assert r.json() == {"message": "Password recovery email sent"}


@pytest.mark.usefixtures("function_create_normaluser")
def test_recovery_password_user_not_exits(
    client: TestClient, normaluser_token_headers: dict[str, str]
) -> None:
    email = f"not-{settings.FIRST_SUPERUSER}"
    r = client.post(
        f"/password-recovery/{email}",
        headers=normaluser_token_headers,
    )
    assert r.status_code == 404


@pytest.mark.usefixtures("function_create_normaluser")
def test_reset_password(
    client: TestClient,
    normaluser_token_headers: dict[str, str],
    db_session: Session,
) -> None:
    token = generate_password_reset_token(email=settings.EMAIL_TEST_USER)
    data = {"new_password": "changethis", "token": token}
    r = client.post(
        "/reset-password/",
        headers=normaluser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    assert r.json() == {"message": "Password updated successfully"}

    user_query = select(User).where(User.email == settings.EMAIL_TEST_USER)
    user = db_session.scalar(user_query)
    assert user
    assert verify_password(data["new_password"], user.hashed_password)


@pytest.mark.usefixtures("function_create_normaluser")
def test_reset_password_invalid_token(
    client: TestClient, normaluser_token_headers: dict[str, str]
) -> None:
    data = {"new_password": "changethis", "token": "invalid"}
    r = client.post(
        "/reset-password/",
        headers=normaluser_token_headers,
        json=data,
    )
    response = r.json()

    assert "detail" in response
    assert r.status_code == 400
    assert response["detail"] == "Invalid token"
