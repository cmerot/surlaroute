import uuid
from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.exc import NoResultFound
from sqlalchemy_utils import Ltree
from sqlmodel import func, or_, select

from app.api.deps import SessionDep
from app.directory.dtos import (
    ActivitiesPublic,
    ActivityCreate,
    ActivityMoveResponse,
    ActivityPublic,
    ActivityUpdate,
    LtreeField,
)
from app.directory.models import (
    Activity,
    ActivityRepository,
    PeoplePublic,
    Person,
    PersonCreate,
    PersonPublic,
    PersonUpdate,
)
from app.utils.dtos import Message

router = APIRouter()


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    skip: int = Field(0, ge=0)
    search: str = Field(default=None, min_length=3, max_length=255)


@router.get("/people", response_model=PeoplePublic)
async def read_people(
    filter_query: Annotated[FilterParams, Query()],
    session: SessionDep,
) -> Any:
    """
    Retrieve people.
    """
    count_statement = select(func.count()).select_from(Person)
    statement = select(Person).offset(filter_query.skip).limit(filter_query.limit)

    if filter_query.search:
        where_clause = or_(
            Person.name.contains(filter_query.search),
            Person.email.contains(filter_query.search),
        )
        count_statement = count_statement.where(where_clause)
        statement = statement.where(where_clause)

    count = session.exec(count_statement).one()
    people = session.exec(statement).all()

    return PeoplePublic(data=people, count=count)


@router.get("/people/{id}", response_model=PersonPublic)
def read_person_by_id(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get person by ID.
    """
    person = session.get(Person, id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.post("/people", response_model=PersonPublic)
def create_person(*, session: SessionDep, person_in: PersonCreate) -> Any:
    """
    Create new person.
    """
    person = Person.model_validate(person_in)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@router.patch("/people/{id}", response_model=PersonPublic)
def update_person(
    *,
    session: SessionDep,
    id: uuid.UUID,
    person_in: PersonUpdate,
) -> Any:
    """
    Update a person.
    """
    person = session.get(Person, id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    update_dict = person_in.model_dump(exclude_unset=True)
    person.sqlmodel_update(update_dict)
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@router.delete("/people/{id}")
def delete_person(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete a person.
    """
    person = session.get(Person, id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    session.delete(person)
    session.commit()
    return Message(message="Person deleted successfully")


@router.post("/activities", response_model=ActivityPublic)
def create_activity(*, session: SessionDep, activity_in: ActivityCreate) -> Any:
    """
    Create new activity.
    """
    activity = Activity(**activity_in.model_dump())
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity


@router.get("/activities", response_model=ActivitiesPublic)
def read_activities(session: SessionDep) -> Any:
    """
    Retrieve activities.
    """
    statement = select(Activity).order_by(Activity.path.asc())
    activities = session.scalars(statement).all()
    return {"data": activities}


@router.get("/activities/{path}", response_model=ActivitiesPublic | ActivityPublic)
def read_activities_by_path(
    session: SessionDep, path: str, descendant: bool = False
) -> Any:
    """
    Retrieve activities.
    """
    if descendant:
        statement = select(Activity).filter(Activity.path.descendant_of(Ltree(path)))
        activities = session.scalars(statement).all()
        return {"data": activities}
    else:
        statement = select(Activity).where(Activity.path == Ltree(path))
        try:
            activity = session.scalar(statement)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Activity not found")

        return activity


@router.patch("/activities/move", response_model=ActivityMoveResponse)
def move_activity(*, session: SessionDep, source: LtreeField, dest: LtreeField) -> Any:
    """
    Move activity from source to dest, including children.
    """
    repository = ActivityRepository(session)
    try:
        lca, rowcount = repository.move(source, dest)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return {"lca": lca, "rowcount": rowcount}


@router.patch("/activities/update/{path}", response_model=ActivityPublic)
def update_activity(
    *, session: SessionDep, path: str, activity_in: ActivityUpdate
) -> Any:
    """
    Retrieve activities.
    """
    statement = select(Activity).where(Activity.path == Ltree(path))

    try:
        activity = session.scalar(statement)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_dict = activity_in.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(activity, key, value)
    session.add(activity)

    try:
        session.commit()
        session.refresh(activity)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error while updating activity: {e}"
        )
    return activity
