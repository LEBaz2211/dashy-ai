from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db.common_models import Dashboard, Task, Tag, TaskList
from ai_service.db.schemas import TaskCreate, TaskUpdate, TaskSearchWithUser
from ai_service.db.schemas.task import TaskWithDetails

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise ValueError(f"No task found with ID {task_id}")

    if task_data.title is not None:
        db_task.title = task_data.title
    if task_data.dueDate is not None:
        db_task.dueDate = task_data.dueDate
    if task_data.reminder is not None:
        db_task.reminder = task_data.reminder
    if task_data.notes is not None:
        db_task.notes = task_data.notes

    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_for_tagging(db: Session, task_ids: List[int]):
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()
    return tasks

def update_task_tags(db: Session, task_id: int, tags: List[str]):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.tags = []
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            task.tags.append(tag)
        db.commit()
        db.refresh(task)
    return task

def search_tasks_with_user(db: Session, search_params: TaskSearchWithUser) -> List[TaskWithDetails]:
    query = db.query(Task, TaskList, Dashboard) \
              .join(Task.taskList) \
              .join(TaskList.dashboard) \
              .filter(Dashboard.userId == search_params.user_id)

    if search_params.title:
        query = query.filter(Task.title.contains(search_params.title))
    if search_params.tag:
        query = query.join(Task.tags).filter(Tag.name == search_params.tag)
    if search_params.completed is not None:
        query = query.filter(Task.completed == search_params.completed)

    results = query.all()

    tasks = []
    for task, task_list, dashboard in results:
        task_data = task.__dict__
        task_data["task_list_title"] = task_list.title
        task_data["dashboard_title"] = dashboard.title
        tasks.append(task_data)

    return tasks
