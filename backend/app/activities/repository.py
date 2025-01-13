from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import Ltree

from app.core.db.models import Activity
from app.core.schemas import PageParams


def get_activity(
    *,
    session: Session,
    path: str | Ltree,
) -> Activity:
    statement = select(Activity).where(Activity.path == Ltree(path))
    return session.scalars(statement).one()


def get_activities(
    *,
    session: Session,
    path: str | None = None,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[Activity], int]:
    count_statement = select(func.count()).select_from(Activity)
    statement = (
        select(Activity)
        .order_by(Activity.path.asc())
        .offset(page_params.offset)
        .limit(page_params.limit)
    )

    if path is not None and path != "":
        filter_clause = Activity.path.descendant_of(Ltree(path))
        statement = statement.filter(filter_clause)
        count_statement = count_statement.filter(filter_clause)

    count = session.scalars(count_statement).one()
    activities = session.scalars(statement).all()
    return activities, count
