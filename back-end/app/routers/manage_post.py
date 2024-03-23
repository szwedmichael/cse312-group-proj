from fastapi import APIRouter, Depends
from app.services.manage_post import ManagePostService
from app.models.manage_post import AddPostModel, PostInteractionModel


router = APIRouter()


@router.post("/add-post")
async def add_post(
    add_post_info: AddPostModel, manage_post_service: ManagePostService = Depends()
):
    return manage_post_service.addPost(
        add_post_info.authToken, add_post_info.xsrf, add_post_info.post
    )


@router.post("/like-post")
async def like_post(
    like_post_info: PostInteractionModel,
    manage_post_service: ManagePostService = Depends(),
):
    return manage_post_service.likePost(
        like_post_info.post_id,
        like_post_info.authToken,
    )


@router.post("/unlike-post")
async def unlike_post(
    unlike_post_info: PostInteractionModel,
    manage_post_service: ManagePostService = Depends(),
):
    return manage_post_service.unlikePost(
        unlike_post_info.post_id,
        unlike_post_info.authToken,
    )


@router.get("/all-posts")
async def all_posts(manage_post_service: ManagePostService = Depends()):
    # TODO: use function made to list
    # return manage_post_service.listPosts(
    # )
    return
