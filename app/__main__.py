# __main.py
""" Main application
"""
import logging

from fastapi import FastAPI

from .routers import posts, users

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
