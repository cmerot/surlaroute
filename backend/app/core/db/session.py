from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def get_db() -> Generator[Session, None, None]:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
