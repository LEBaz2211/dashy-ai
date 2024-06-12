from typing import List, Optional
from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime

from ai_service.db.schemas.dashboard import Dashboard

class UserBase(BaseModel):
    name: Optional[str]
    email: str

class UserCreate(UserBase):
    password: Optional[str] = None
    image: Optional[str] = None
    emailVerified: Optional[datetime] = None

class User(UserBase):
    id: str
    dashboards: List['Dashboard'] = []

    class Config:
        orm_mode = True

class UserCreateWithImage(BaseModel):
    name: Optional[str]
    email: str
    password: Optional[str] = None
    image: Optional[UploadFile] = None

class UserUpdateWithImage(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str] = None
    image: Optional[UploadFile] = None
