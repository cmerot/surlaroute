#!/usr/bin/env python
import logging
import os

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from alembic import command
from alembic.config import Config
from app.core.config import settings
from app.core.db.session import get_db
from app.users import crud
from app.users.schemas import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("prestart")


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def test_db(session: Session) -> None:
    session.execute(select(1))
    logger.info("Database ready")


def create_db_extensions(session: Session) -> None:
    session.execute(text("CREATE EXTENSION IF NOT EXISTS ltree"))
    session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    session.commit()


def create_first_superuser(session: Session) -> None:
    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
        is_active=True,
    )
    try:
        crud.create_user(session=session, user_create=user_in)
        session.commit()
        logger.info("Superuser created")
        print("Superuser created")
    except IntegrityError:
        logger.info("Superuser already exists")
        print("Superuser already exists")


def upgrade_to_head() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_cfg = Config(os.path.join(script_dir, "../alembic.ini"))

    # Perform the upgrade to the head revision
    command.upgrade(alembic_cfg, "head")
    command.check(alembic_cfg)


if __name__ == "__main__":
    session = next(get_db())
    logger.info("Waiting for database to be ready")
    test_db(session=session)

    logger.info("Creating postgresql extensions")
    create_db_extensions(session=session)

    logger.info("Running alembic upgrade")
    upgrade_to_head()

    # For some reason (alembic.ini?) alembic changes the log level
    # so this wont appear
    logger.info("Creating first superuser")
    print("Creating first superuser")
    create_first_superuser(session=session)

    logging.shutdown()
