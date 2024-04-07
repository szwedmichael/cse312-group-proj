from fastapi import APIRouter, Depends, Cookie, Response, UploadFile, WebSocket
from app.services.manage_post import ManagePostService
from app.models.manage_post import PostModel, PostInteractionModel
from typing import Union

router = APIRouter()


# Supposedly allows body data and multipart upload
# https://github.com/tiangolo/fastapi/issues/2257#issuecomment-726843164
@router.post("/add-post")
async def add_post(
    response: Response,
    add_post_info: PostModel = Depends(),
    file: Union[UploadFile, None] = None,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.addPost(add_post_info, file, auth_token)


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


# websocket_route
@router.websocket("/ws-posts")
async def ws_posts(
    websocket: WebSocket,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
    file: Union[UploadFile, None] = None,
):
    await websocket.accept()
    while True:
        response = Response()
        response.headers["X-Content-Type-Options"] = "nosniff"
        data = await websocket.receive_json()
        ret_msg = None
        if data["action"] == "add":
            ret_msg = manage_post_service.addPost(data, file, auth_token)
        elif data["action"] == "like":
            ret_msg = manage_post_service.likePost(data["post_id"], auth_token)
        elif data["action"] == "unlike":
            ret_msg = manage_post_service.unlikePost(
                data["post_id"],
                auth_token,
            )
        elif data["action"] == "list":
            ret_msg = manage_post_service.listPosts()
        await websocket.send_json(ret_msg)
