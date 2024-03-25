from pydantic import BaseModel
from datetime import datetime


class PostModel(BaseModel):
    location: str
    description: str
    date: str


class PostInteractionModel(BaseModel):
    post_id: str
