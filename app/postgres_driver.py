# postgres.py

import logging
import os

import psycopg
from psycopg.rows import dict_row

from .models import Post

logger = logging.getLogger(__name__)


def get_conn_str() -> str:
    """Get connection string for postgres database.

    Raises:
        KeyError: When any of the required env variables is not found
    """
    return (
        f"dbname={os.environ['POSTGRES_DB']} "
        f"user={os.environ['POSTGRES_USER']} "
        f"password={os.environ['POSTGRES_PASSWORD']} "
        f"host={os.environ['POSTGRES_HOST']} "
        f"port={os.environ['POSTGRES_PORT']}"
    )


def get_all_posts():
    with psycopg.connect(get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts """)
            posts = cursor.fetchall()
            return posts


def get_post(id: int):
    with psycopg.connect(get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
            post = cursor.fetchone()
            return post


def insert_post(post: Post):
    with psycopg.connect(get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published),
            )
            new_post = cursor.fetchone()
            return new_post


def delete_post(id: int):
    with psycopg.connect(get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),)
            )
            deleted_post = cursor.fetchone()
            return deleted_post


def update_post(id: int, post: Post):
    with psycopg.connect(get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                (post.title, post.content, post.published, str(id)),
            )
            updated_post = cursor.fetchone()
            return updated_post
