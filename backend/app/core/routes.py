from fastapi import APIRouter

from app.directory import router
from app.tours import router as tour_router
from app.users import routes_login, routes_users
from app.utils import routes as routes_utils

api_router = APIRouter()
api_router.include_router(routes_login.router, tags=["login"])
api_router.include_router(routes_users.router, prefix="/users", tags=["users"])
api_router.include_router(routes_utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(router.router, prefix="/directory")
api_router.include_router(tour_router.router, prefix="/tours", tags=["tours"])
