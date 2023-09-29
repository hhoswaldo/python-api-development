# users.py
""" Users router"""

import logging

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..core import config, schemas

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    user.password = config.hash(user.password)
    new_user = db.users.create_user(user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int):
    user = db.users.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user
