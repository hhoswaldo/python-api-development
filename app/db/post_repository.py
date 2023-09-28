import logging
from typing import List

import psycopg
from psycopg.rows import DictRow, dict_row

from app.core.config import get_postgres_conn_str
from app.models.post import Post

logger = logging.getLogger(__name__)


def get_all_posts() -> List[DictRow]:
    with psycopg.connect(get_postgres_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts """)
            posts = cursor.fetchall()
            return posts


def get_post(post_id: int) -> DictRow | None:
    with psycopg.connect(get_postgres_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(post_id),))
            post = cursor.fetchone()
            return post


def insert_post(post: Post) -> DictRow | None:
    with psycopg.connect(get_postgres_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published),
            )
            new_post = cursor.fetchone()
            return new_post


def delete_post(post_id: int) -> DictRow | None:
    with psycopg.connect(get_postgres_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(post_id),)
            )
            deleted_post = cursor.fetchone()
            return deleted_post


def update_post(post_id: int, post: Post) -> DictRow | None:
    with psycopg.connect(get_postgres_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                (post.title, post.content, post.published, str(post_id)),
            )
            updated_post = cursor.fetchone()
            return updated_post
