from pydantic import BaseModel


class PostModel(BaseModel):
    location: str
    description: str
    date: str
    day: str
    month: int
    year: int
    minute: int
    hour: int


class PostInteractionModel(BaseModel):
    post_id: str
