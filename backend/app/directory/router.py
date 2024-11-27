from fastapi import APIRouter

from app.directory import routes_activity, routes_org, routes_person

router = APIRouter()

router.include_router(routes_activity.router, prefix="/activities", tags=["activities"])
router.include_router(routes_person.router, prefix="/people", tags=["people"])
router.include_router(routes_org.router, prefix="/orgs", tags=["orgs"])
