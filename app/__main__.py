# __main.py
""" Main application
"""
import logging

from fastapi import FastAPI, HTTPException, Response, status

from .routers import posts

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(posts.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
