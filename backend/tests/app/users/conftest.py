import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db.models import User
from app.core.security import get_password_hash


@pytest.fixture(scope="function")
def function_create_normaluser(db_session: Session) -> User:
    """Function-scoped fixture that creates a new user for each test."""
    user = User(
        email=settings.EMAIL_TEST_USER,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        is_active=True,
    )

    db_session.add(user)
    db_session.flush()

    return user  # Return the user object directly since we're using the same session


@pytest.fixture(scope="function")
def normaluser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.EMAIL_TEST_USER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture(autouse=True)
def clear_users(db_session: Session) -> None:
    """Clear users before each test."""
    db_session.execute(text('DELETE FROM "user"'))
    db_session.commit()
