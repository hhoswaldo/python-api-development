import logging
from typing import List

import psycopg
from psycopg.rows import DictRow, dict_row

from ..core import config

logger = logging.getLogger(__name__)


def get_vote_by_user_id(user_id: int, post_id: int):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ SELECT * FROM votes WHERE user_id = %s AND post_id = %s""",
                (str(user_id), str(post_id)),
            )
            post = cursor.fetchone()
    return post


def create_vote(user_id: int, post_id: int, vote_direction: bool):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO votes (post_id, user_id, direction) VALUES (%s, %s, %s) RETURNING * """,
                (post_id, user_id, vote_direction),
            )
            new_vote = cursor.fetchone()
    return new_vote


def delete_vote(user_id: int, post_id: int):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ DELETE from votes WHERE post_id = %s AND user_id = %s """,
                (post_id, user_id),
            )
