import pytest
from sqlalchemy.orm import Session

from app.core.db.models import Tour
from tests.conftest import random_lower_string


@pytest.fixture(scope="function")
def function_create_tours(db_session: Session) -> None:
    """Function-scoped fixture that creates 10 Tour."""
    for _ in range(10):
        tour = Tour(name=random_lower_string())
        db_session.add(tour)
    db_session.flush()


# @pytest.fixture(autouse=True)
# def clear_users(db_session: Session) -> None:
#     """Clear users before each test."""
#     db_session.execute(text('DELETE FROM "user"'))
#     db_session.commit()
