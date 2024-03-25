from fastapi import APIRouter, Depends, Cookie
from fastapi.responses import JSONResponse, Response
from app.services.homepage import HomepageService
from typing import Union


router = APIRouter()


@router.get("/user-details")
async def user_details(
    response: Response,
    homepage_service: HomepageService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return homepage_service.getName(auth_token)


@router.get("/verify-auth")
async def verify_auth(
    response: Response,
    homepage_service: HomepageService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return homepage_service.checkUser(auth_token)
