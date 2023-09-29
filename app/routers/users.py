import logging
from typing import List

import psycopg
from fastapi import APIRouter, HTTPException, Response, status
from psycopg.rows import dict_row

from ..core import config, schemas

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate):
    user.password = config.hash(user.password)

    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """ INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """,
                (user.email, user.password),
            )
            new_user = cursor.fetchone()
            logger.debug(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int):
    with psycopg.connect(config.get_conn_str(), row_factory=dict_row) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM users WHERE id = %s """, (str(user_id),))
            user = cursor.fetchone()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user
