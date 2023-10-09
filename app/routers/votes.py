# votes.py
import logging
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from .. import db
from ..core import oauth2, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(
    vote: schemas.Vote, current_user: Dict = Depends(oauth2.get_current_user)
):
    post = db.posts.get_post_by_id(vote.post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.post_id} does not exist",
        )
    user_id = current_user["id"]
    vote_query = db.votes.get_vote_by_user_id(user_id, vote.post_id)
    logger.debug(vote_query)
    if vote.direction:
        if vote_query is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user_id} has already voted on post {vote.post_id}",
            )
        _ = db.votes.create_vote(user_id, vote.post_id, vote.direction)
        return {"message": "Successfully added vote"}
    if vote_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
        )
    db.votes.delete_vote(user_id, vote.post_id)
    return {"message": "Successfully deleted vote"}
