from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.directory.schemas import PageParams
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User(**user_create.model_dump(exclude={"password"}))
    db_obj.hashed_password = get_password_hash(user_create.password)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def read_users(
    *,
    session: Session,
    page_params: PageParams = PageParams(),
) -> tuple[Sequence[User], int]:
    count_statement = select(func.count()).select_from(User)
    statement = select(User).offset(page_params.offset).limit(page_params.limit)
    count = session.scalars(count_statement).one()
    users = session.scalars(statement).all()
    return users, count


def update_user(
    *,
    session: Session,
    db_user: User,
    user_in: UserUpdate,
) -> User:
    for key, value in user_in.model_dump(exclude_unset=True).items():
        if key == "password":
            db_user.hashed_password = get_password_hash(value)
        else:
            setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).filter(User.email == email)
    session_user = session.scalar(statement)
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
