from fastapi import APIRouter
from app.api.routers import users, login, pollution
api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pollution.router, prefix="/pollution", tags=["pollution"])
api_router.include_router(login.router, tags=["login"])
