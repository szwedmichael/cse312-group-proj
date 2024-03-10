from fastapi import APIRouter, Depends
from app.services.example import ExampleService
from app.models.signup import SignupModel

router = APIRouter()


@router.get("/signup")
async def example(
    user_signup_info: SignupModel, service: ExampleService = Depends(ExampleService)
):
    return
    # return service.do_something_in_service()
