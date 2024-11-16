from sqlalchemy import Session, select

from app.users.models import User


def read_people(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(User).offset(skip).limit(limit)).all()
