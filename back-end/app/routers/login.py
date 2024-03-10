from fastapi import APIRouter, Depends
from app.services.example import ExampleService
from app.models.login import LoginModel

router = APIRouter()


@router.get("/login")
async def some_login_logic(
    user_login_info: LoginModel, service: ExampleService = Depends(ExampleService)
):
    return
    # return service.do_something_in_service()
