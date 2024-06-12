from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import enum

class TaskType(str, enum.Enum):
    auto_subtask = 'auto_subtask'
    auto_tag = 'auto_tag'
    auto_ranking = 'auto_ranking'
    general_assistance = 'general_assistance'

class AITaskBase(BaseModel):
    task_type: TaskType
    related_task_id: Optional[List[int]] = None
    user_id: str
    ai_output: str

class AITaskCreate(AITaskBase):
    pass

class AITask(AITaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
