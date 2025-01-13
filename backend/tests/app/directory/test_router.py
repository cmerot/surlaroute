import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.db.models import Org, Person


@pytest.mark.usefixtures("function_create_actors", "function_create_superuser")
def test_get_all_actors_endpoint(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.get("/directory/", headers=superuser_token_headers)
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["total"] == 20  # Ensure total count matches
    assert len(json_response["results"]) == 10  # Ensure results match the limit


@pytest.mark.usefixtures("function_create_actors")
def test_get_org_endpoint(client: TestClient, db_session: Session):
    org = Org(name="test_org", other_read=True)
    db_session.add(org)
    db_session.flush()

    response = client.get(f"/directory/orgs/{org.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == org.name  # Ensure the org name matches


def test_get_org_not_found_endpoint(client: TestClient):
    non_existent_id = uuid.uuid4()

    response = client.get(f"/directory/orgs/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"  # Ensure the correct error message


@pytest.mark.usefixtures("function_create_actors")
def test_get_person_endpoint(client: TestClient, db_session: Session):
    person = Person(name="test_person", other_read=True)
    db_session.add(person)
    db_session.flush()

    response = client.get(f"/directory/people/{person.id}")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == person.name  # Ensure the person name matches


def test_get_person_not_found_endpoint(client: TestClient):
    non_existent_id = uuid.uuid4()

    response = client.get(f"/directory/people/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"  # Ensure the correct error message
