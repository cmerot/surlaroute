import logging

from sqlalchemy import Engine, text
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))

    except Exception as e:
        logger.error(e)
        raise e

    # Create required PostgreSQL extensions
    session.exec(text("CREATE EXTENSION IF NOT EXISTS ltree"))
    session.exec(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    session.commit()


def main() -> None:
    logger.info("Waiting for database to be ready")
    init(engine)
    logger.info("Database ready")


if __name__ == "__main__":
    main()
