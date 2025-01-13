import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.activities.repository import get_activity
from app.core.db.models import Activity


def test_get_activity(db_session: Session) -> None:
    # Arrange: Create a test activity
    test_activity = Activity(path="test.path", name="test")
    db_session.add(test_activity)
    db_session.flush()

    # Act: Retrieve the activity using the get_activity function
    retrieved_activity = get_activity(session=db_session, path="test.path")

    # Assert: Check that the retrieved activity matches the test activity
    assert retrieved_activity.path == test_activity.path


def test_get_activity_not_found(db_session: Session) -> None:
    # Act & Assert: Check that a NoResultFound exception is raised for a non-existent activity
    with pytest.raises(NoResultFound):
        get_activity(session=db_session, path="non.existent.path")
