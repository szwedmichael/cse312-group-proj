from fastapi import APIRouter, Depends
from app.services.user_auth import UserAuthService
from app.models.user_auth import LoginModel, SignupModel

router = APIRouter()


@router.post("/login")
async def login(
    user_login_info: LoginModel, user_auth_service: UserAuthService = Depends()
):
    return user_auth_service.loginUser(
        user_login_info.username, user_login_info.password
    )


@router.post("/signup")
async def signup(
    user_signup_info: SignupModel, user_auth_service: UserAuthService = Depends()
):
    return user_auth_service.registerUser(
        user_signup_info.username,
        user_signup_info.password,
        user_signup_info.passwordConfirmation,
    )


@router.post("/logout")
async def logout(user_auth_service: UserAuthService = Depends()):
    EXTRACTED_AUTH_COOKIE = None
    return user_auth_service.logoutUser(EXTRACTED_AUTH_COOKIE)
