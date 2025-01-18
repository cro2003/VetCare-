from fastapi import APIRouter
from app.routers.api_v1.auth import auth_route

home_router = APIRouter()
home_router.include_router(auth_route, prefix='/auth', tags=['auth'])

@home_router.get('/')
async def home():
    return {
        "msg": "Welcome"
    }