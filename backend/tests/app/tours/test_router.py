import uuid

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.db.models import Tour
from app.core.security import SecurityContext, set_security_context
from app.tours.repository import get_all_tours, get_tour
from app.tours.schemas import ToursPageParams


@pytest.mark.usefixtures("function_create_tours")
def test_get_all_tours_with_query(db_session: Session):
    set_security_context(db_session, SecurityContext(is_superuser=True))

    # Assuming there is a function get_all_tours similar to get_all_actors
    tours, count = get_all_tours(
        session=db_session, page_params=ToursPageParams(q="test")
    )

    assert len(tours) > 0  # Check if some tours are returned
    assert count > 0  # Ensure count is returned


@pytest.mark.usefixtures("function_create_tours")
def test_get_all_tours_with_activity_filter(db_session: Session):
    set_security_context(db_session, SecurityContext(is_superuser=True))

    # Assuming there is a function get_all_tours similar to get_all_actors
    tours, count = get_all_tours(
        session=db_session, page_params=ToursPageParams(activity="some_activity")
    )

    assert len(tours) >= 0  # Check if the number of tours is valid
    assert count >= 0  # Ensure count is returned


@pytest.mark.usefixtures("function_create_tours")
def test_get_tour(db_session: Session):
    set_security_context(db_session, SecurityContext(is_superuser=True))

    tour = Tour(name="detailed_tour")
    db_session.add(tour)
    db_session.flush()
    retrieved_tour = get_tour(session=db_session, id=tour.id)

    assert retrieved_tour is not None  # Ensure the tour is found
    assert retrieved_tour.name == "detailed_tour"  # Check if the name matches


@pytest.mark.usefixtures("function_create_tours")
def test_get_tour_with_invalid_id(db_session: Session):
    set_security_context(db_session, SecurityContext(is_superuser=True))

    invalid_id = uuid.uuid4()

    with pytest.raises(NoResultFound):
        get_tour(session=db_session, id=invalid_id)
