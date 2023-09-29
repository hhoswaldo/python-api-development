import logging

import psycopg
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from psycopg.rows import dict_row

from .. import db
from ..core import config, oauth2, schemas

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = db.users.get_user_by_username(credentials.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    if not config.verify(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
