from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import prisma_crud, schemas, database

router = APIRouter()

@router.post("/feedback", response_model=schemas.Feedback)
async def create_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(database.get_db_ai)):
    return prisma_crud.create_feedback(db, feedback)

@router.get("/tasks/{task_id}", response_model=schemas.Task)
async def get_task(task_id: int, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", response_model=schemas.Task)
async def delete_task(task_id: int, db: Session = Depends(database.get_db_prisma)):
    task = prisma_crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/tasks/{task_id}/subtasks", response_model=schemas.Subtask)
async def create_subtask(task_id: int, subtask: schemas.SubtaskCreate, db: Session = Depends(database.get_db_prisma)):
    return prisma_crud.create_subtask(db, subtask)

@router.put("/tasks/{task_id}/subtasks/{subtask_id}", response_model=schemas.Subtask)
async def update_subtask(task_id: int, subtask_id: int, subtask_update: schemas.SubtaskUpdate, db: Session = Depends(database.get_db_prisma)):
    subtask = prisma_crud.update_subtask(db, subtask_id, subtask_update)
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.post("/tasks/{task_id}/tags", response_model=schemas.Tag)
async def create_tag(task_id: int, tag: schemas.TagCreate, db: Session = Depends(database.get_db_prisma)):
    return prisma_crud.create_tag(db, tag)

@router.delete("/tasks/{task_id}/tags/{tag_id}", response_model=schemas.Tag)
async def delete_tag(task_id: int, tag_id: int, db: Session = Depends(database.get_db_prisma)):
    tag = prisma_crud.delete_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.get("/tasks/{task_id}/ai-tasks", response_model=List[schemas.AITask])
async def get_ai_tasks_for_task(task_id: int, db: Session = Depends(database.get_db_ai)):
    return prisma_crud.get_ai_tasks_by_task_id(db, task_id)

@router.post("/search/tasks", response_model=List[schemas.TaskWithDetails])
async def search_tasks(search_params: schemas.TaskSearchWithUser, db: Session = Depends(database.get_db_prisma)):
    tasks = prisma_crud.search_tasks_with_user(db, search_params)
    return tasks


