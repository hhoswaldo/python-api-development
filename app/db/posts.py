# posts.py
""" CRUD operations for posts table
"""
import logging
from typing import List

import psycopg
from psycopg.rows import DictRow, dict_row

from ..core import config, schemas

logger = logging.getLogger(__name__)


def create_post(post: schemas.PostCreate) -> DictRow | None:
    logger.debug(post)
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published, post.user_id),
            )
            new_post = cursor.fetchone()
    return new_post


def get_post_by_id(post_id: int) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(post_id),))
            post = cursor.fetchone()
    return post


def delete_post_by_id(post_id: int) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id),)
            )
            deleted_post = cursor.fetchone()
    return deleted_post


def update_post_by_id(post_id: int, post: schemas.PostUpdate) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                (post.title, post.content, post.published, str(post_id)),
            )
            updated_post = cursor.fetchone()
    return updated_post


def get_all_posts() -> List[DictRow]:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts """)
            posts = cursor.fetchall()
    return posts
