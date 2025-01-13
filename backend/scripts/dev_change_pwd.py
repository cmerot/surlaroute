#!/usr/bin/env python


import os

from app.core.db.models import User
from app.core.db.session import get_db
from app.core.security import get_password_hash

if __name__ == "__main__":
    email = os.getenv("SLR_EMAIL") or input("Email:")
    password = os.getenv("SLR_PASSWORD") or input("Password:")

    db = next(get_db())

    u = db.query(User).filter(User.email == email).one()
    u.hashed_password = get_password_hash(password)
    db.add(u)
    db.commit()
