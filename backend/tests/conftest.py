import random
import string
from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import Session, SessionTransaction, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import settings
from app.core.db.models import Base, User
from app.core.db.session import get_db
from app.core.routes import api_router
from app.core.security import get_password_hash


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_test_db_url() -> str:
    """Get database URL from environment or use default test database."""
    return str(settings.SQLALCHEMY_DATABASE_URI) + "_tests"


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine, None, None]:
    """Create test database and return engine instance."""
    database_url = get_test_db_url()

    # Create database if it doesn't exist
    if not database_exists(database_url):
        create_database(database_url)
        print(f"Created test database: {database_url}")

    # Create engine with NullPool to ensure connections are closed
    engine = create_engine(
        database_url,
        poolclass=NullPool,
    )

    # Set up database with required extensions
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS ltree"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.commit()

    Base.metadata.create_all(engine)

    yield engine

    # Optional: Drop database after all tests
    if database_exists(database_url):
        drop_database(database_url)


@pytest.fixture(scope="session")
def db_session_factory(
    db_engine: Engine,
) -> sessionmaker[Session]:
    """Create a factory for database sessions."""
    return sessionmaker(bind=db_engine)


@pytest.fixture(scope="function")
def db_session(
    db_session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """Create a new database session for a test."""
    session = db_session_factory()

    # Start transaction
    session.begin_nested()

    # Set up savepoint
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session: Session, transaction: SessionTransaction) -> None:
        if transaction.nested and (
            not transaction._parent or not transaction._parent.nested
        ):
            session.begin_nested()

    yield session

    # Rollback and close session
    session.rollback()
    session.close()


# @pytest.fixture(scope="module")
# def module_session(
#     db_session_factory: sessionmaker[Session],
# ) -> Generator[Session, None, None]:
#     """Create a module-scoped session that persists data across tests within a module."""
#     session = db_session_factory()

#     yield session

#     # Cleanup at the end of the module
#     session.rollback()
#     session.close()


@pytest.fixture(scope="function")
def db_setup(db_session: Session) -> Generator[Session, None, None]:
    """Setup test database state and handle cleanup.

    Use this fixture when you need to set up initial test data.
    """
    yield db_session


# Add cleanup fixture if needed for specific cleanup tasks
@pytest.fixture(scope="function", autouse=True)
def cleanup_db(db_session: Session) -> Generator[Session, None, None]:
    """Clean up any test data after each test."""
    yield db_session

    # Add any specific cleanup logic here if needed
    db_session.rollback()


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    App is a fixture so it can be overriden by the client.
    """
    app = FastAPI()
    app.include_router(api_router)
    yield app


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db() -> Generator[Session, Any, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def function_create_superuser(db_session: Session) -> User:
    """Function-scoped fixture that creates a new user for each test."""
    user = User(
        email=settings.FIRST_SUPERUSER,
        hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        is_active=True,
        is_superuser=True,
    )

    db_session.add(user)
    db_session.flush()

    return user  # Return the user object directly since we're using the same session


@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
