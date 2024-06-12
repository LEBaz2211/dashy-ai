from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .tag import Tag
from .subtask import Subtask

class TaskBase(BaseModel):
    title: str
    completed: Optional[bool] = False
    taskListId: int
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None

class Task(BaseModel):
    id: int
    title: str
    completed: bool
    dueDate: Optional[datetime]
    reminder: Optional[datetime]
    notes: Optional[str]
    tags: List[Tag]
    subtasks: List[Subtask]

    class Config:
        orm_mode = True

class TaskSearchWithUser(BaseModel):
    user_id: str
    title: Optional[str] = None
    completed: Optional[bool] = None
    tag: Optional[str] = None

class TaskWithDetails(BaseModel):
    id: int
    title: str
    completed: bool
    taskListId: int
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None
    task_list_title: str
    dashboard_title: str
    tags: List[str] = []
    subtasks: List[str] = []

    class Config:
        from_attributes = True
