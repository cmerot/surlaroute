#!/usr/bin/env python
# mypy: ignore-errors


from app.core.db.models import User
from app.core.db.session import SessionLocal
from app.core.security import get_password_hash

db = SessionLocal()

if __name__ == "__main__":
    u = db.query(User).filter(User.email == "cmerot@themarqueeblink.com").one()
    u.hashed_password = get_password_hash("changethis")
    db.add(u)
    db.commit()
