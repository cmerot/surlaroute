import uuid

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Tour, User
from app.tours.repository import get_all_tours, get_tour
from app.tours.schemas import ToursPageParams


@pytest.mark.usefixtures("function_create_tours")
def test_get_all_tours(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)

    # Assuming there is a function get_all_tours similar to get_all_actors
    tours, count = get_all_tours(session=db_session)

    assert len(tours) == 10  # Check if the number of tours is within the limit
    assert count == 10  # Ensure count is returned


@pytest.mark.usefixtures("function_create_tours")
def test_get_all_tours_paginated(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)

    # Assuming there is a function get_all_tours similar to get_all_actors
    tours, count = get_all_tours(
        session=db_session, page_params=ToursPageParams(limit=5)
    )

    assert len(tours) == 5  # Check if the number of tours is within the limit
    assert count == 10  # Ensure count is returned


def test_get_tour(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    tour = Tour(name="test_tour")
    db_session.add(tour)
    db_session.flush()
    tour = get_tour(session=db_session, id=tour.id)

    assert tour is not None  # Ensure the tour is found


def test_get_tour_not_found(db_session: Session):
    db_session.info["user"] = User(is_superuser=True)
    non_existent_id = uuid.uuid4()

    with pytest.raises(NoResultFound):
        get_tour(session=db_session, id=non_existent_id)
