from typing import List
from pydantic import BaseModel

class TaskTagUpdate(BaseModel):
    task_id: int
    tags: List[str]

class AutoTagRequest(BaseModel):
    tasks: List[int]
    user_id: str

class AutoTagResponse(BaseModel):
    updated_tasks: List[TaskTagUpdate]
    ai_task_id: int

class AutoSubtaskRequest(BaseModel):
    tasks: List[int]
    user_id: str

class SubtaskUpdate(BaseModel):
    task_id: int
    subtasks: List[str]

class AutoSubtaskResponse(BaseModel):
    updated_tasks: List[SubtaskUpdate]
    ai_task_id: int
