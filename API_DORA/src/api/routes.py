from fastapi import APIRouter

from src.api.endpoints.auth import router as auth_endpoint
from src.api.endpoints.characters import router as characters_endpoint
from src.api.endpoints.requests import router as request_endpoint


routers = [auth_endpoint, characters_endpoint, request_endpoint]


api_router = APIRouter(prefix="/api")

for router in routers:
    api_router.include_router(router)
