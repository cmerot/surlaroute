from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import settings
from app.core.db.base_class import Base
from app.core.db.session import get_db
from app.core.routes import api_router
from scripts.run_pre_start import create_db_extensions, create_first_superuser
from tests.directory.fixtures import (
    activity_fixtures,
    om_fixtures,
    organisation_fixtures,
    person_fixtures,
)
from tests.users.user import (
    authentication_token_from_email,
    get_superuser_token_headers,
)


@pytest.fixture(scope="session")
def engine() -> Engine:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI) + "_tests")

    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    with Session(engine) as session:
        create_db_extensions(session=session)
        Base.metadata.create_all(engine)
        create_first_superuser(session=session)

    return engine


@pytest.fixture(scope="session")
def session(engine: Engine) -> Generator[Session, Any, None]:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="session", autouse=True)
def populated_db(session: Session) -> None:
    session.add_all(activity_fixtures)
    session.add_all(person_fixtures)
    session.add_all(organisation_fixtures)
    session.add_all(om_fixtures)
    session.commit()


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    """
    App is a fixture so it can be overriden by the client.
    """
    app = FastAPI()
    app.include_router(api_router)
    yield app


@pytest.fixture(scope="module")
def client(app: FastAPI, session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db() -> Generator[Session, Any, None]:
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, session: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=session
    )
