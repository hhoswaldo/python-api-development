from random import randrange
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts: List[Dict] = [{"title": "post_1", "content": "bla bla bla", "id": 1}]


def find_post(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_data = post.model_dump()
    post_data["id"] = randrange(0, 1_000_000)
    my_posts.append(post_data)
    return {"data": post_data}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    print(index)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )
    post_deserialized = post.model_dump()
    post_deserialized["id"] = id
    my_posts[index] = post_deserialized
    return {"data": post_deserialized}
