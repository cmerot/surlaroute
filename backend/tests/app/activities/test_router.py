from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.db.models import Activity


def test_get_activities_by_path(client: TestClient, db_session: Session) -> None:
    # Arrange: Create a test activity
    test_activity = Activity(path="test.path", name="Test Activity")
    db_session.add(test_activity)
    db_session.flush()

    # Act: Retrieve the activity using the router endpoint
    response = client.get("/activities/test.path")
    json_response = response.json()

    # Assert: Check that the response is successful and matches the test activity
    assert response.status_code == 200
    assert json_response["name"] == test_activity.name
    assert json_response["path"] == test_activity.path


def test_get_activities_by_path_not_found(client: TestClient) -> None:
    # Act: Attempt to retrieve a non-existent activity
    response = client.get("/activities/non.existent.path")

    # Assert: Check that a 404 error is returned
    assert response.status_code == 404
    assert response.json()["detail"] == "Catégorie non trouvée"
