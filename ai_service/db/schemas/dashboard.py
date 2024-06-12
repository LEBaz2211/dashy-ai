from typing import List
from pydantic import BaseModel

from ai_service.db.schemas.tasklist import TaskList

class DashboardBase(BaseModel):
    title: str
    userId: str

class DashboardCreate(DashboardBase):
    pass

class Dashboard(DashboardBase):
    id: int
    taskLists: List['TaskList'] = []

    class Config:
        orm_mode = True
