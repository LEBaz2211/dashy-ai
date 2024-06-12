from typing import Optional
from pydantic import BaseModel

class SubtaskBase(BaseModel):
    title: str
    completed: Optional[bool] = False
    taskId: int

class SubtaskCreate(SubtaskBase):
    pass

class Subtask(SubtaskBase):
    id: int

    class Config:
        orm_mode = True

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = False
