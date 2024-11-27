import json

from fastapi.testclient import TestClient

from app.core.schemas import DeleteResponse, PagedResponse
from app.directory.crud_schemas import (
    ActivityPublic,
)


def test_create_activity(client: TestClient) -> None:
    # Post an activity
    content = {"path": "a1"}
    r = client.post("/directory/activities", content=json.dumps(content))
    assert r.status_code == 200

    activity = ActivityPublic.model_validate_json(json.dumps(r.json()))
    assert activity
    assert activity.path == "a1"
    assert activity.name == "a1"

    # Re-post the same
    r = client.post("/directory/activities", content=json.dumps(content))
    assert r.status_code == 400

    # Another one with parent_path
    content = {"name": "a2", "path": "a1.a2"}
    r = client.post("/directory/activities", content=json.dumps(content))
    assert r.status_code == 200

    activity = ActivityPublic.model_validate_json(json.dumps(r.json()))
    assert activity.path == "a1.a2"
    assert activity.name == "a2"


def test_read_activities(client: TestClient) -> None:
    r = client.get("/directory/activities")
    json_resp = r.json()
    assert PagedResponse[ActivityPublic].model_validate_json(json.dumps(json_resp))
    assert r.status_code == 200
    assert len(json_resp["results"]) == 13


def test_read_activities_by_path(client: TestClient) -> None:
    r = client.get("/directory/activities/cat")
    json_resp = r.json()
    assert r.status_code == 200
    assert ActivityPublic.model_validate_json(json.dumps(json_resp))


def test_read_activities_by_path_with_descendant(client: TestClient) -> None:
    r = client.get("/directory/activities/cat?descendant=true")
    json_resp = r.json()
    resp = PagedResponse[ActivityPublic].model_validate_json(json.dumps(json_resp))
    assert r.status_code == 200
    assert len(resp.results) == 13


def test_update_activity(client: TestClient) -> None:
    content = {"name": "a1bis"}
    r = client.patch("/directory/activities/a1", content=json.dumps(content))
    assert r.status_code == 200

    content = {"dest_path": "cat.a1"}
    r = client.patch("/directory/activities/a1", content=json.dumps(content))
    assert r.status_code == 200

    content = {"name": "miaou", "dest_path": "cat.wild.a1"}
    r = client.patch("/directory/activities/cat.a1", content=json.dumps(content))
    assert r.status_code == 200


def test_delete_activity(client: TestClient) -> None:
    r = client.delete("/directory/activities/cat.wild")
    response = DeleteResponse.model_validate_json(json.dumps(r.json()))
    assert r.status_code == 200
    assert response.data["total"] == 2  # type: ignore[index]

    r = client.delete("/directory/activities/cat.wild.miaou")
    response = DeleteResponse.model_validate_json(json.dumps(r.json()))
    assert r.status_code == 200
    assert response.data["total"] == 0  # type: ignore[index]
