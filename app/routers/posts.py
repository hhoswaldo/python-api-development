# posts.py
import logging

from fastapi import APIRouter, HTTPException, Response, status

from ..db import post_repository
from ..models.post import Post

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/posts")
def get_posts():
    return {"data": post_repository.get_all_posts()}


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    return {"data": post_repository.insert_post(post)}


@router.get("/posts/{post_id}")
def get_post(post_id: int):
    post = post_repository.get_post(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} was not found",
        )
    return {"data": post}


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    deleted_post = post_repository.delete_post(post_id)
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    updated_post = post_repository.update_post(post_id, post)
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )
    return {"data": updated_post}
