from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .ai_task import TaskType

class FeedbackBase(BaseModel):
    task_type: TaskType
    ai_task_id: int
    user_id: str
    feedback: str
    rating: Optional[int] = None  # Optional rating (1-5)

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
