from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.core.db.session import SessionDep
from app.core.schemas import (
    DeleteResponse,
    PagedResponse,
    PageParamsDep,
    UpdateResponse,
)
from app.directory import crud
from app.directory.crud_schemas import (
    ActivityCreate,
    ActivityPublic,
    ActivityUpdate,
)

router = APIRouter()


@router.post("/", response_model=ActivityPublic)
def create_activity(
    *, session: SessionDep, activity_create: ActivityCreate
) -> ActivityPublic:
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
    return ActivityPublic.model_validate(activity)


@router.get("/{path}", response_model=PagedResponse[ActivityPublic] | ActivityPublic)
def read_activities_by_path(
    session: SessionDep,
    path: str,
    page_params: PageParamsDep,
    descendant: bool = False,
) -> PagedResponse[ActivityPublic] | ActivityPublic:
    """
    Read activities from a path.
    """
    if descendant is False:
        try:
            activity = crud.read_activity(session=session, path=path)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Activity not found")
        return ActivityPublic.model_validate(activity)
    else:
        try:
            results, total = crud.read_activities(
                session=session, path=path, page_params=page_params
            )
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Activity not found")

        return PagedResponse[ActivityPublic].model_validate(
            {
                "total": total,
                "limit": page_params.limit,
                "offset": page_params.offset,
                "results": results,
            }
        )


@router.get("/", response_model=PagedResponse[ActivityPublic])
def read_activities(
    session: SessionDep, page_params: PageParamsDep
) -> PagedResponse[ActivityPublic]:
    """
    Read all activities.
    """
    results, total = crud.read_activities(session=session)
    return PagedResponse[ActivityPublic].model_validate(
        {
            "total": total,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": results,
        }
    )


@router.patch("/{path}", response_model=UpdateResponse[ActivityPublic])
def update_activity(
    *, session: SessionDep, path: str, entity_in: ActivityUpdate
) -> UpdateResponse[ActivityPublic]:
    """
    Update an activity.

    If the name or the parent path is patched, it will also update children.
    """
    try:
        data = crud.update_activity(session=session, path=path, entity_in=entity_in)
        session.commit()
    except NoResultFound:
        session.rollback()
        raise HTTPException(status_code=404, detail="Activity not found")

    return UpdateResponse[ActivityPublic].model_validate(
        {
            "success": True,
            "data": data,
        }
    )


@router.delete("/{path}", response_model=DeleteResponse)
def delete_activity(*, session: SessionDep, path: str) -> DeleteResponse:
    """
    Delete an activity and its children.
    """
    total = crud.delete_activity(session=session, path=path)
    session.commit()

    return DeleteResponse.model_validate(
        {
            "success": True,
            "message": f"Activity {path} deleted",
            "data": {"total": total},
        }
    )
