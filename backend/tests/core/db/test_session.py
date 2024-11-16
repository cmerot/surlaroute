from app.core.db.session import get_db


def test_get_db() -> None:
    session = next(get_db())
    assert (
        f"{session.__module__}.{session.__class__.__name__}"
        == "sqlalchemy.orm.session.Session"
    )
