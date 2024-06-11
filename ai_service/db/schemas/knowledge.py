from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import enum

class KnowledgeType(str, enum.Enum):
    project = 'project'
    object = 'object'
    course = 'course'
    preference = 'preference'
    other = 'other'

class UserKnowledgeBase(BaseModel):
    user_id: str
    type: KnowledgeType
    content: str

class UserKnowledgeCreate(UserKnowledgeBase):
    pass

class UserKnowledge(UserKnowledgeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
