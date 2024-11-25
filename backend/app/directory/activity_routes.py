from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.core.db.models import Activity
from app.core.db.session import SessionDep
from app.core.schemas import PagedResponse
from app.directory import activity_crud as crud
from app.directory.activity_schemas import (
    ActivitiesPublic,
    ActivityCreate,
    ActivityDeleteResponse,
    ActivityPublic,
    ActivityUpdate,
    ActivityUpdateResponse,
)

router = APIRouter()


@router.post("/", response_model=ActivityPublic)
def create_activity(
    *, session: SessionDep, activity_create: ActivityCreate
) -> Activity:
    """
    Create an activity.
    """
    try:
        activity = crud.create_activity(
            session=session, activity_create=activity_create
        )
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Path '{activity.path}' already exists.",
        )
    return activity


@router.get("/{path}", response_model=PagedResponse[ActivityPublic])
def read_activities_by_path(
    session: SessionDep, path: str, descendant: bool = False
) -> Any:
    """
    Read activities from a path.
    """
    if descendant is False:
        try:
            activity = crud.read_activity(session=session, path=path)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity
    else:
        try:
            result = crud.read_activities(session=session, path=path)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Activity not found")
        return {"data": result}


@router.get("/", response_model=ActivitiesPublic)
def read_activities(session: SessionDep) -> Any:
    """
    Read all activities.
    """
    activities = crud.read_activities(session=session)
    return ActivitiesPublic.model_validate({"data": activities})


@router.patch("/{path}", response_model=ActivityUpdateResponse)
def update_activity(
    *, session: SessionDep, path: str, activity_update: ActivityUpdate
) -> ActivityUpdateResponse:
    """
    Update an activity.

    If the name or the parent path is patched, it will also update children.
    """
    try:
        lca, rowcount = crud.update_activity(
            session=session, path=path, activity_update=activity_update
        )
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(status_code=404, detail="Activity not found")

    return ActivityUpdateResponse(lca=lca, rowcount=rowcount)


@router.delete("/{path}", response_model=ActivityDeleteResponse)
def delete_activity(*, session: SessionDep, path: str) -> Any:
    """
    Delete an activity and its children.
    """
    rowcount = crud.delete_activity(session=session, path=path)
    session.commit()
    return {"rowcount": rowcount}
