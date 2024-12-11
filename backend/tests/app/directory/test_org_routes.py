import json
import uuid

from fastapi.testclient import TestClient

from app.core.schemas import PagedResponse, UpdateResponse
from app.directory.crud_schemas import (
    OrgPublic,
)
from tests.app.directory.fixtures import org_fixtures


def test_read_org_by_id(client: TestClient) -> None:
    r = client.get(f"/directory/orgs/{org_fixtures[0].id}")
    result = r.json()
    assert r.status_code == 200
    assert OrgPublic.model_validate_json(json.dumps(result))


def test_read_org_not_found(client: TestClient) -> None:
    r = client.get(f"/directory/orgs/{uuid.uuid4()}")
    assert r.status_code == 404


def test_read_orgs(client: TestClient) -> None:
    r = client.get("/directory/orgs")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrgPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == len(org_fixtures)


def test_read_orgs_limit(client: TestClient) -> None:
    r = client.get("/directory/orgs?limit=1")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrgPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == 1


def test_read_orgs_offset(client: TestClient) -> None:
    r = client.get("/directory/orgs?offset=2")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrgPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == len(org_fixtures) - 2


def test_read_orgs_limit_offset(client: TestClient) -> None:
    r = client.get("/directory/orgs?offset=1&limit=2")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrgPublic].model_validate_json(json.dumps(result))
    assert orgs.results[0].id == org_fixtures[1].id


def test_update_org(client: TestClient) -> None:
    data = {"name": "updated"}
    org = org_fixtures[0]
    r = client.patch(f"/directory/orgs/{org.id}", content=json.dumps(data))
    result = r.json()
    assert r.status_code == 200
    resp = UpdateResponse[OrgPublic].model_validate_json(json.dumps(result))
    assert resp
