import uuid
from unittest.mock import Mock, create_autospec

import pytest
from sqlalchemy.orm import Session

from app.core.security import (
    SecurityContext,
    get_security_context,
    set_security_context,
    set_security_context_from_user,
)


@pytest.fixture
def mock_session():
    mock_session = create_autospec(Session, instance=True)
    mock_session.info = {}
    return mock_session


def test_set_security_context(mock_session):
    # Arrange
    mock_session.info = {}
    security_context = SecurityContext(
        user_id=uuid.uuid4(),
        is_superuser=True,
        is_member=True,
        group_ids=[uuid.uuid4(), uuid.uuid4()],
    )

    # Act
    set_security_context(mock_session, security_context)
    session_security_context = get_security_context(mock_session)

    # Assert
    assert session_security_context == security_context


def test_set_security_context_from_user(mock_session):
    # Arrange
    user_id = uuid.uuid4()
    user = Mock(
        id=user_id,
        is_superuser=True,
        is_member=True,
        person=Mock(
            membership_assocs=[Mock(org_id=uuid.uuid4()), Mock(org_id=uuid.uuid4())]
        ),
    )
    mock_session.scalar.return_value = user

    # Act
    set_security_context_from_user(mock_session, user)
    security_context = get_security_context(mock_session)

    # Assert
    assert security_context.user_id == user_id
    assert security_context.is_superuser is True
    assert security_context.is_member is True
    assert len(security_context.group_ids) == 2
    mock_session.expunge_all.assert_called_once()


##


def test_set_security_context_from_user_no_person(mock_session):
    # Arrange
    user_id = uuid.uuid4()
    user = Mock(
        id=user_id,
        is_superuser=True,
        is_member=True,
        person=None,
    )
    mock_session.scalar.return_value = user

    # Act
    set_security_context_from_user(mock_session, user)
    security_context = get_security_context(mock_session)

    # Assert
    assert security_context.user_id == user_id
    assert security_context.is_superuser is True
    assert security_context.is_member is True
    assert len(security_context.group_ids) == 0
    mock_session.expunge_all.assert_called_once()
