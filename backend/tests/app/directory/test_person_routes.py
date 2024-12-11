import json
import uuid

from fastapi.testclient import TestClient

from app.core.schemas import PagedResponse
from app.directory.crud_schemas import (
    PersonPublic,
)
from tests.app.directory.fixtures import person_fixtures


def test_read_person_by_id(client: TestClient) -> None:
    r = client.get(f"/directory/people/{person_fixtures[0].id}")
    result = r.json()
    assert r.status_code == 200
    assert PersonPublic.model_validate_json(json.dumps(result))


def test_read_person_not_found(client: TestClient) -> None:
    r = client.get(f"/directory/people/{uuid.uuid4()}")
    assert r.status_code == 404


def test_read_people(client: TestClient) -> None:
    r = client.get("/directory/people")
    result = r.json()
    assert r.status_code == 200
    assert PagedResponse[PersonPublic].model_validate_json(json.dumps(result))


def test_read_people_limit(client: TestClient) -> None:
    r = client.get("/directory/people?limit=1")
    result = r.json()
    assert r.status_code == 200
    assert PagedResponse[PersonPublic].model_validate_json(json.dumps(result))


def test_read_people_offset(client: TestClient) -> None:
    r = client.get("/directory/people?offset=2")
    result = r.json()
    assert r.status_code == 200
    assert PagedResponse[PersonPublic].model_validate_json(json.dumps(result))


def test_read_people_limit_offset(client: TestClient) -> None:
    r = client.get("/directory/people?offset=1&limit=2")
    result = r.json()
    assert r.status_code == 200
    assert PagedResponse[PersonPublic].model_validate_json(json.dumps(result))
