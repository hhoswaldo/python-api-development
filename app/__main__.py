# __main.py
""" Main application
"""
import logging

from fastapi import FastAPI, HTTPException, Response, status

from app.driver import posts_ops
from app.driver.models import Post

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": posts_ops.get_all_posts()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    return {"data": posts_ops.insert_post(post)}


@app.get("/posts/{id}")
def get_post(id: int):
    post = posts_ops.get_post(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    deleted_post = posts_ops.delete_post(id)
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    updated_post = posts_ops.update_post(id, post)
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    return {"data": updated_post}
