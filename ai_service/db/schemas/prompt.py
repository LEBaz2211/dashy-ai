from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import enum

class PromptType(str, enum.Enum):
    auto_tag = 'auto_tag'
    auto_subtask = 'auto_subtask'
    auto_ranking = 'auto_ranking'
    general = 'general'

class PersonalizedPromptBase(BaseModel):
    user_id: str
    prompt: str
    type: PromptType

class PersonalizedPromptCreate(PersonalizedPromptBase):
    pass

class PersonalizedPrompt(PersonalizedPromptBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
