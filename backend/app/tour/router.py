from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.db.session import SessionDep
from app.directory import crud
from app.directory.crud_schemas import (
    TreeCreate,
    TreePublic,
)

router = APIRouter()


@router.post("/", response_model=TreePublic)
def create_activity(*, session: SessionDep, activity_create: TreeCreate) -> TreePublic:
    """
    Create an activity.
    """
    try:
        activity = crud.create_activity(session=session, entity_in=activity_create)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Path '{activity.path}' already exists.",
        )
    return TreePublic.model_validate(activity)
