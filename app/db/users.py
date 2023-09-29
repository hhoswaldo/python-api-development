import psycopg
from psycopg.rows import DictRow, dict_row

from ..core import config, schemas


def get_user_by_username(username: str) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM users WHERE email = %s """, (username,))
            user = cursor.fetchone()
    return user


def get_user_by_id(user_id: int) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM users WHERE id = %s """, (str(user_id),))
            user = cursor.fetchone()
    return user


def create_user(user: schemas.UserCreate) -> DictRow | None:
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """,
                (user.email, user.password),
            )
            new_user = cursor.fetchone()
    return new_user
