from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound

from app.activities import repository
from app.activities.schemas import TreePublic
from app.core.db.session import SessionDep
from app.core.schemas import (
    PagedResponse,
    PageParamsDep,
)

router = APIRouter()


@router.get("/{path}", response_model=PagedResponse[TreePublic] | TreePublic)
def get_activities_by_path(
    session: SessionDep,
    path: str,
    page_params: PageParamsDep,
    descendant: bool = False,
) -> PagedResponse[TreePublic] | TreePublic:
    """
    Read activities from a path.
    """
    if descendant is False:
        try:
            activity = repository.get_activity(session=session, path=path)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")
        return TreePublic.model_validate(activity)
    else:
        try:
            results, total = repository.get_activities(
                session=session, path=path, page_params=page_params
            )
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")

        return PagedResponse[TreePublic].model_validate(
            {
                "total": total,
                "limit": page_params.limit,
                "offset": page_params.offset,
                "results": results,
            }
        )


@router.get("/", response_model=PagedResponse[TreePublic])
def get_activities(
    session: SessionDep, page_params: PageParamsDep
) -> PagedResponse[TreePublic]:
    """
    Read all activities.
    """
    results, total = repository.get_activities(session=session, page_params=page_params)
    return PagedResponse[TreePublic].model_validate(
        {
            "total": total,
            "limit": page_params.limit,
            "offset": page_params.offset,
            "results": results,
        }
    )
