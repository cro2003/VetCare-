from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import ResponseTime
from app.routers import home_router
from app.routers.api_v1.auth import auth_route


def get_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ResponseTime)

    app.include_router(home_router, prefix='')

    return app