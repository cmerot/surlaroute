import uuid
from collections.abc import Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.db.models import Tour
from app.core.schemas import PageParams


def read_tour(
    *,
    session: Session,
    id: uuid.UUID,
) -> Tour:
    return session.get_one(Tour, id)


def read_tours(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Tour], int]:
    count_statement = select(func.count()).select_from(Tour)
    statement = select(Tour).offset(page_params.offset).limit(page_params.limit)

    if page_params.q:
        where_clause = or_(
            Tour.name.icontains(page_params.q),
        )
        count_statement = count_statement.where(where_clause)
        statement = statement.where(where_clause)

    count = session.scalars(count_statement).one()
    tours = session.scalars(statement).all()
    return tours, count
