import json

from fastapi.testclient import TestClient

from app.directory.activity_schemas import (
    ActivitiesPublic,
    ActivityDeleteResponse,
    ActivityPublic,
)


def test_create_activities(client: TestClient) -> None:
    # Post an activity
    data = {"name": "a1"}
    r = client.post("/directory/activities", content=json.dumps(data))
    assert r.status_code == 200

    activity = ActivityPublic.model_validate_json(json.dumps(r.json()))
    assert activity
    assert activity.path == "a1"
    assert activity.name == "a1"

    # Re-post the same
    r = client.post("/directory/activities", content=json.dumps(data))
    assert r.status_code == 400

    # Another one with parent_path
    data = {"name": "a2", "parent_path": "a1"}
    r = client.post("/directory/activities", content=json.dumps(data))
    assert r.status_code == 200

    activity = ActivityPublic.model_validate_json(json.dumps(r.json()))
    assert activity.path == "a1.a2"
    assert activity.name == "a2"


def test_update_activity(client: TestClient) -> None:
    data = {"name": "a1bis"}
    r = client.patch("/directory/activities/a1", content=json.dumps(data))
    assert r.status_code == 200

    data = {"parent_path": "cat"}
    r = client.patch("/directory/activities/a1bis", content=json.dumps(data))
    assert r.status_code == 200

    data = {"name": "miaou", "parent_path": "cat.wild"}
    r = client.patch("/directory/activities/cat.a1bis", content=json.dumps(data))
    assert r.status_code == 200


# def test_read_activities(client: TestClient) -> None:
#     r = client.get("/directory/activities")
#     result = r.json()
#     assert r.status_code == 200
#     assert result["data"]
#     assert result["data"][0]["id"]
#     assert result["data"][0]["name"]
#     assert result["data"][0]["path"]
#     assert len(result["data"]) == 13


def test_read_activities_by_path(client: TestClient) -> None:
    r = client.get("/directory/activities/cat")
    result = r.json()
    assert r.status_code == 200
    assert ActivityPublic.model_validate_json(json.dumps(result))


def test_read_activities_by_path_with_descendant(client: TestClient) -> None:
    r = client.get("/directory/activities/cat?descendant=true")
    result = r.json()
    assert r.status_code == 200
    assert ActivitiesPublic.model_validate_json(json.dumps(result))


def test_delete_activity(client: TestClient) -> None:
    r = client.delete("/directory/activities/cat.wild.miaou")
    response = ActivityDeleteResponse.model_validate_json(json.dumps(r.json()))

    assert r.status_code == 200
    assert response.rowcount == 2

    r = client.delete("/directory/activities/cat.wild.miaou")
    response = ActivityDeleteResponse.model_validate_json(json.dumps(r.json()))

    assert r.status_code == 200
    assert response.rowcount == 0
