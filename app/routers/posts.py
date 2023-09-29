# posts.py
import logging
from typing import List

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Response, status
from psycopg.rows import dict_row

from ..core import config, oauth2, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts():
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts """)
            posts = cursor.fetchall()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, user_id: int = Depends(oauth2.get_current_user)
):
    logger.debug("User id: %d", user_id)
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published),
            )
            new_post = cursor.fetchone()
    return new_post


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(post_id),))
            post = cursor.fetchone()
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id),)
            )
            deleted_post = cursor.fetchone()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                (post.title, post.content, post.published, str(post_id)),
            )
            updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} does not exist",
        )
    return updated_post
