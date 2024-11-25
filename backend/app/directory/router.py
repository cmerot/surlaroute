from fastapi import APIRouter

from app.directory import activity_routes, org_routes, person_routes

router = APIRouter()

router.include_router(activity_routes.router, prefix="/activities", tags=["activities"])
router.include_router(person_routes.router, prefix="/people", tags=["people"])
router.include_router(org_routes.router, prefix="/orgs", tags=["orgs"])
