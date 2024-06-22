from typing import Annotated
from fastapi import APIRouter, Depends

from src.api.schemas import UserLogin, UserRegister, SignInResponse
from src.api.services.auth_service import AuthService, auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(user_login_info: UserLogin, auth_service: Annotated[AuthService, Depends(auth_service)]) -> (
        SignInResponse):
    response = await auth_service.sign_in(user_login_info)
    return response


@router.post("/sign-up")
async def sign_up(user_register_info: UserRegister, auth_service: Annotated[AuthService, Depends(auth_service)]) -> (
        SignInResponse):
    response = await auth_service.sign_up(user_register_info)
    return response
