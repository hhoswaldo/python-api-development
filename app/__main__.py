# __main.py
""" Main application
"""
import logging
import logging.config

from fastapi import FastAPI

from .core import config, database, models
from .routers import auth, posts, users, votes

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(votes.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
