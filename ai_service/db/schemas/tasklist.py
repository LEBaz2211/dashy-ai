from typing import List
from pydantic import BaseModel

from ai_service.db.schemas.task import Task

class TaskListBase(BaseModel):
    title: str
    dashboardId: int

class TaskListCreate(TaskListBase):
    pass

class TaskList(TaskListBase):
    id: int
    tasks: List['Task'] = []

    class Config:
        orm_mode = True
