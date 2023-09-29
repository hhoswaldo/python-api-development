# schemas.py
from datetime import datetime
from typing import Optional

from pydantic import AwareDatetime, BaseModel, EmailStr


class PostBase(BaseModel):
    """Post base pydantic model"""

    title: str
    content: str
    published: bool = True


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    """Post pydantic model for Create"""


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: AwareDatetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
