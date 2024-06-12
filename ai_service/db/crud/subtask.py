from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db.common_models import Subtask, Task
from ai_service.db.schemas import SubtaskCreate, SubtaskUpdate

def create_subtask(db: Session, subtask: SubtaskCreate):
    db_subtask = Subtask(**subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

def get_subtask(db: Session, subtask_id: int):
    return db.query(Subtask).filter(Subtask.id == subtask_id).first()

def delete_subtask(db: Session, subtask_id: int):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    db.delete(db_subtask)
    db.commit()

def update_subtask(db: Session, subtask_id: int, subtask_update: SubtaskUpdate):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if db_subtask:
        for key, value in subtask_update.dict().items():
            setattr(db_subtask, key, value)
        db.commit()
        db.refresh(db_subtask)
    return db_subtask

def get_tasks_for_subtasking(db: Session, task_ids: List[int]):
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()
    return tasks

def update_task_subtasks(db: Session, task_id: int, subtask_titles: List[str]):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

    existing_subtasks = db.query(Subtask).filter(Subtask.taskId == task_id).all()
    for subtask in existing_subtasks:
        db.delete(subtask)

    for title in subtask_titles:
        new_subtask = Subtask(title=title, task=task)
        db.add(new_subtask)

    db.commit()
    return task
