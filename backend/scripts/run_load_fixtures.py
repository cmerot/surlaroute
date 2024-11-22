#!/usr/bin/env python
import os

import yaml
from sqlalchemy.orm import Session
from sqlalchemy_utils import Ltree

from app.core.db.session import SessionLocal
from app.directory import activity_crud
from app.directory.models import Activity, Org


def get_path(relative_path: str) -> str:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path
    full_path = os.path.join(script_dir, relative_path)
    return full_path


def load_orgs(db: Session) -> None:
    with open(get_path("../fixtures/orgs.yml")) as f:
        orgs = yaml.safe_load(f)["orgs"]
    print("-" * 80)
    my_list = [1, 2, 3, 4, 5]
    last_element = my_list[-1]
    print(last_element)
    for entity in orgs:
        org = Org(name=entity["name"])

        activity_path = Ltree(entity["activity"])
        try:
            activity_parent_path = activity_path[:-1]
        except Exception:
            activity_parent_path = None
        activity_name = str(activity_path[-1]).title()
        print(f"activity_path: {activity_path}")
        print(f"activity_parent_path: {activity_parent_path}")
        print(f"activity_name: {activity_name}")
        print("---")
        try:
            activity = activity_crud.read_activity(session=db, path=activity_path)
        except Exception:
            activity = Activity(name=activity_name, parent_path=activity_parent_path)
        org.activities.append(activity)
        db.add(org)
        db.flush()


if __name__ == "__main__":
    db = SessionLocal()
    load_orgs(db)
    db.commit()
