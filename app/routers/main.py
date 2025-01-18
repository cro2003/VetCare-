from fastapi import APIRouter
from app.routers.api_v1.auth import auth_route
from app.routers.api_v1.authenticated_user.user import authenticated_user_router

home_router = APIRouter()
home_router.include_router(auth_route, prefix='/auth', tags=['auth'])
home_router.include_router(authenticated_user_router, prefix='/user', tags=['authenticated user'])

@home_router.get('/')
async def home():
    return {
        "msg": "Welcome"
    }