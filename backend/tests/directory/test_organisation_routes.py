import json
import uuid

from fastapi.testclient import TestClient

from app.directory.organisation_schemas import (
    OrganisationPublic,
)
from app.directory.schemas import PagedResponse, UpdateResponse
from tests.directory.fixtures import organisation_fixtures


def test_read_organisation_by_id(client: TestClient) -> None:
    r = client.get(f"/directory/organisations/{organisation_fixtures[0].id}")
    result = r.json()
    assert r.status_code == 200
    assert OrganisationPublic.model_validate_json(json.dumps(result))


def test_read_organisation_not_found(client: TestClient) -> None:
    r = client.get(f"/directory/organisations/{uuid.uuid4()}")
    assert r.status_code == 404


def test_read_organisations(client: TestClient) -> None:
    r = client.get("/directory/organisations")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrganisationPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == len(organisation_fixtures)


def test_read_organisations_limit(client: TestClient) -> None:
    r = client.get("/directory/organisations?limit=1")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrganisationPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == 1


def test_read_organisations_offset(client: TestClient) -> None:
    r = client.get("/directory/organisations?offset=2")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrganisationPublic].model_validate_json(json.dumps(result))
    assert len(orgs.results) == len(organisation_fixtures) - 2


def test_read_organisations_limit_offset(client: TestClient) -> None:
    r = client.get("/directory/organisations?offset=1&limit=2")
    result = r.json()
    assert r.status_code == 200
    orgs = PagedResponse[OrganisationPublic].model_validate_json(json.dumps(result))
    assert orgs.results[0].id == organisation_fixtures[1].id


def test_update_organisation(client: TestClient) -> None:
    data = {"name": "updated"}
    org = organisation_fixtures[0]
    r = client.patch(f"/directory/organisations/{org.id}", content=json.dumps(data))
    result = r.json()
    assert r.status_code == 200
    resp = UpdateResponse[OrganisationPublic].model_validate_json(json.dumps(result))
    assert resp
