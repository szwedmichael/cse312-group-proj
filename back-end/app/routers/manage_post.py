from fastapi import APIRouter, Depends, Cookie, Response
from app.services.manage_post import ManagePostService
from app.models.manage_post import AddPostModel, PostInteractionModel
from typing import Union

router = APIRouter()


@router.post("/add-post")
async def add_post(
    response: Response,
    add_post_info: AddPostModel,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.addPost(
        add_post_info.authToken, add_post_info.xsrf, add_post_info.post, auth_token
    )


@router.post("/like-post")
async def like_post(
    response: Response,
    like_post_info: PostInteractionModel,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.likePost(like_post_info.post_id, auth_token)


@router.post("/unlike-post")
async def unlike_post(
    response: Response,
    unlike_post_info: PostInteractionModel,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.unlikePost(
        unlike_post_info.post_id,
        auth_token,
    )


@router.get("/all-posts")
async def all_posts(
    response: Response, manage_post_service: ManagePostService = Depends()
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.listPosts()
