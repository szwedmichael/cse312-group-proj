from fastapi import APIRouter, Depends, Cookie, Response
from app.services.user_auth import UserAuthService
from app.models.user_auth import LoginModel, SignupModel
from typing import Union

router = APIRouter()


@router.post("/login")
async def login(
    response: Response,
    user_login_info: LoginModel,
    user_auth_service: UserAuthService = Depends(),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return user_auth_service.loginUser(
        user_login_info.username, user_login_info.password
    )


@router.post("/signup")
async def signup(
    response: Response,
    user_signup_info: SignupModel,
    user_auth_service: UserAuthService = Depends(),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return user_auth_service.registerUser(
        user_signup_info.username,
        user_signup_info.password,
        user_signup_info.passwordConfirmation,
    )


@router.post("/logout")
async def logout(
    response: Response,
    user_auth_service: UserAuthService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return user_auth_service.logoutUser(auth_token)
