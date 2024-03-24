from fastapi import APIRouter, Depends, Cookie
from app.services.homepage import HomepageService
from typing import Union


router = APIRouter()


@router.get("/user-details")
async def user_details(
    homepage_service: HomepageService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    return


@router.get("/verify-auth")
async def verify_auth(
    homepage_service: HomepageService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    return homepage_service.checkUser(auth_token)
