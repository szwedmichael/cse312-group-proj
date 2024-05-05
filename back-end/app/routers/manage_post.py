from fastapi import APIRouter, Depends, Cookie, Response, UploadFile, WebSocket, Form
from app.services.manage_post import ManagePostService
from app.models.manage_post import PostModel, PostInteractionModel
from typing import Union, List
from starlette.websockets import WebSocketDisconnect

router = APIRouter()


# Supposedly allows body data and multipart upload
# https://github.com/tiangolo/fastapi/issues/2257#issuecomment-726843164
@router.post("/add-post")
async def add_post(
    response: Response,
    location: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    day: str = Form(...),
    month: int = Form(...),
    hour: int = Form(...),
    year: int = Form(...),
    minute: int = Form(...),
    file: Union[UploadFile, None] = None,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
):
    add_post_info = PostModel(location=location, description=description, date=date, day=day, month = month, year=year, minute=minute, hour=hour)
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

@router.get("/random-posts")
async def random_posts(
    response: Response, manage_post_service: ManagePostService = Depends()
):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return manage_post_service.randomizePosts()

# this will store active webSocket connections
active_websockets: List[WebSocket] = []
# this will broadcast the message to all active websockets
async def broadcast(data):
    for websocket in active_websockets:
        try:
            await websocket.send_json(data)
        except WebSocketDisconnect:
            active_websockets.remove(websocket)

@router.websocket("/ws-posts")
async def ws_posts(
    websocket: WebSocket,
    manage_post_service: ManagePostService = Depends(),
    auth_token: Union[str, None] = Cookie(None),
    file: Union[UploadFile, None] = None,
):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            response = Response()
            response.headers["X-Content-Type-Options"] = "nosniff"
            data = await websocket.receive_json()
            ret_msg = None
            if data["action"] == "like":
                ret_msg = manage_post_service.likePost(data["post_id"], auth_token)
            elif data["action"] == "unlike":
                ret_msg = manage_post_service.unlikePost(data["post_id"], auth_token)
            
            # broadcast the response to all clients
            await broadcast(ret_msg)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
