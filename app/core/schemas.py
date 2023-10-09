# schemas.py
from datetime import datetime
from typing import Optional

from pydantic import AwareDatetime, BaseModel, EmailStr


class PostBase(BaseModel):
    """Post base pydantic model"""

    title: str
    content: str
    published: bool = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class PostCreate(PostBase):
    """Post CREATE pydantic model"""

    user_id: Optional[int] = None


class PostUpdate(PostBase):
    """Post UPDATE pydantic model"""


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


class Vote(BaseModel):
    post_id: int
    direction: bool = True
