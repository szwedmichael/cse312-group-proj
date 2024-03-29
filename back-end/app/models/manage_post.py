from pydantic import BaseModel


class PostModel(BaseModel):
    location: str
    description: str
    date: str


class PostInteractionModel(BaseModel):
    post_id: str
