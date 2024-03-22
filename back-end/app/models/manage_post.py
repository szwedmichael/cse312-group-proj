from pydantic import BaseModel
from datetime import datetime


class PostModel(BaseModel):
    location: str
    description: str
    date: datetime


class AddPostModel(BaseModel):
    post: PostModel
    authToken: str
    xsrf: str


class PostInteractionModel(BaseModel):
    post_id: str
    authToken: str
