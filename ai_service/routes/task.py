from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import crud
from ..db import database, prisma_crud
from ..db import schemas
from ai_service.db.schemas import TaskCreate, TaskUpdate, SubtaskCreate, SubtaskUpdate, Task, Subtask, TaskWithDetails, TaskSearchWithUser, Feedback, FeedbackCreate

router = APIRouter()

@router.post("/feedback", response_model=Feedback)
async def create_feedback(feedback: FeedbackCreate, db: Session = Depends(database.get_db_ai)):
    return prisma_crud.create_feedback(db, feedback)

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(database.get_db_prisma)):
    try:
        updated_task = prisma_crud.update_task(db, task_id, task)
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, db: Session = Depends(database.get_db_prisma)):
    return prisma_crud.create_task(db, task)

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks/{task_id}/subtasks", response_model=Subtask)
async def create_subtask(task_id: int, subtask: SubtaskCreate, db: Session = Depends(database.get_db_prisma)):
    return prisma_crud.create_subtask(db, subtask)

@router.put("/tasks/{task_id}/subtasks/{subtask_id}", response_model=Subtask)
async def update_subtask(task_id: int, subtask_id: int, subtask_update: SubtaskUpdate, db: Session = Depends(database.get_db_prisma)):
    subtask = prisma_crud.update_subtask(db, subtask_id, subtask_update)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.post("/tasks/{task_id}/tags", response_model=Task)
def add_tag_to_task(task_id: int, tag: schemas.TagCreate, db: Session = Depends(database.get_db_prisma)):
    try:
        task = prisma_crud.add_tag_to_task(db, task_id, tag.name)
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Remove a tag from a task
@router.delete("/tasks/{task_id}/tags/{tag_id}", response_model=Task)
def remove_tag_from_task(task_id: int, tag_id: int, db: Session = Depends(database.get_db_prisma)):
    try:
        task = prisma_crud.remove_tag_from_task(db, task_id, tag_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/tasks/{task_id}/ai-tasks", response_model=List[schemas.AITask])
async def get_ai_tasks_for_task(task_id: int, db: Session = Depends(database.get_db_ai)):
    return crud.get_ai_tasks_by_task_id(db, task_id)

@router.post("/search/tasks", response_model=List[TaskWithDetails])
async def search_tasks(search_params: TaskSearchWithUser, db: Session = Depends(database.get_db_prisma)):
    tasks = prisma_crud.search_tasks_with_user(db, search_params)
    return tasks


