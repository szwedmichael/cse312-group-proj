from fastapi import Depends
from app.repos.example import ExampleRepo


class ExampleService:
    def __init__(self, example_repository: ExampleRepo = Depends(ExampleRepo)):
        self.repo = example_repository

    def do_something_in_service(self):
        return self.repo.get_index()
