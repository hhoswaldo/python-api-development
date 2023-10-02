# posts.py
import logging
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import db
from ..core import oauth2, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "/",
    response_model=List[schemas.PostResponse],
)
def get_posts(
    _: Dict = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    return db.posts.get_posts_with_limit_offset_search(limit, skip, search)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.PostCreate, current_user: Dict = Depends(oauth2.get_current_user)
):
    post.user_id = current_user["id"]
    new_post = db.posts.create_post(post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, _: Dict = Depends(oauth2.get_current_user)):
    post = db.posts.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found",
        )
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int, current_user: Dict = Depends(oauth2.get_current_user)
):
    post = db.posts.get_post_by_id(post_id)

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} does not exist",
        )

    if post["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    db.posts.delete_post_by_id(post_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    current_user: Dict = Depends(oauth2.get_current_user),
):
    post_to_update = db.posts.get_post_by_id(post_id)

    if post_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )

    if post_to_update["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    updated_post = db.posts.update_post_by_id(post_id, post)

    return updated_post
