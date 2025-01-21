from fastapi import APIRouter

from app.activities import router as activities_router
from app.directory import router as directory_router
from app.explore import router as explore_router
from app.tours import router as tour_router
from app.users import router_login, router_users
from app.utils import routes as router_utils

api_router = APIRouter()
api_router.include_router(explore_router.router, prefix="/explore", tags=["explore"])
api_router.include_router(tour_router.router, prefix="/tours", tags=["tours"])
api_router.include_router(
    directory_router.router, prefix="/directory", tags=["directory"]
)
api_router.include_router(router_login.router, tags=["login"])
api_router.include_router(router_users.router, tags=["users"], prefix="/users")
api_router.include_router(router_utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(
    activities_router.router, tags=["activities"], prefix="/activities"
)
