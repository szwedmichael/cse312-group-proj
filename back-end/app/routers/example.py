from fastapi import APIRouter, Depends
from app.services.example import ExampleService

router = APIRouter()


@router.get("/example")
async def example(service: ExampleService = Depends(ExampleService)):
    return
    # return service.do_something_in_service()
