from collections.abc import Sequence

from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session
from sqlalchemy_utils import Ltree

from app.directory.activity_schemas import (
    ActivityCreate,
    ActivityUpdate,
)
from app.directory.models import Activity
from app.directory.schemas import PageParams


def create_activity(
    *,
    session: Session,
    activity_create: ActivityCreate,
) -> Activity:
    db_obj = Activity(**activity_create.model_dump())
    session.add(db_obj)
    return db_obj


def read_activity(
    *,
    session: Session,
    path: str | Ltree,
) -> Activity:
    statement = select(Activity).where(Activity.path == Ltree(path))
    return session.scalars(statement).one()


def read_activities(
    *,
    session: Session,
    path: str | None = None,
    page_params: PageParams = PageParams(),  # noqa: ARG001
) -> tuple[Sequence[Activity], int]:
    statement = select(Activity).order_by(Activity.path.asc())
    if path is not None and path != "":
        statement = statement.filter(Activity.path.descendant_of(Ltree(path)))
    activities = session.scalars(statement).all()
    return activities


def update_activity(
    *,
    session: Session,
    path: str,
    activity_update: ActivityUpdate,
) -> tuple[Ltree | None, int]:
    """
    Update activity. Updating parent_path and/or name will update children.
    """

    activity = read_activity(session=session, path=path)
    source = activity.path
    if activity_update.parent_path is not None:
        dest = activity_update.parent_path + activity.path[-1]
        activity.path = dest
    if activity_update.name is not None:
        try:
            dest = dest[:-1] + activity_update.name
            activity.path = dest
        except UnboundLocalError:
            activity.name = Activity.slugify(activity_update.name)
            dest = activity.path

    return _rename_activity(session=session, source=source, dest=dest)


def delete_activity(*, session: Session, path: str) -> int:
    statement = delete(Activity).filter(Activity.path.descendant_of(Ltree(path)))
    cursor = session.execute(statement)
    return cursor.rowcount


def _rename_activity(
    *, session: Session, source: str | Ltree, dest: str | Ltree
) -> tuple[Ltree | None, int]:
    source = Ltree(source)

    if dest == "":
        pass
    else:
        dest = Ltree(dest)

    statement = text(
        f"UPDATE {Activity.__tablename__} "
        f"SET {Activity.path.key} = "
        f"    CASE WHEN nlevel({Activity.path.key}) = nlevel('{source}') THEN '{dest}' "
        f"         ELSE '{dest}' || subpath({Activity.path.key}, nlevel('{source}')) "
        f"     END "
        f"WHERE {Activity.path.key} <@ '{source}'"
    )
    cursor = session.execute(statement)

    if dest == "":
        lca = None
    else:
        lca = source.lca(dest)  # type: ignore[arg-type]

    return lca, cursor.rowcount  # type: ignore[attr-defined]
