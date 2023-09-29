# posts.py
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from .. import db
from ..core import oauth2, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(current_user: int = Depends(oauth2.get_current_user)):
    return db.posts.get_all_posts()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user)):
    logger.debug("Current user: %s", current_user)
    new_post = db.posts.create_post(post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, current_user: int = Depends(oauth2.get_current_user)):
    post = db.posts.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {post_id} not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.posts.delete_post_by_id(post_id)
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.posts.update_post_by_id(post_id, post)
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )
    return updated_post
