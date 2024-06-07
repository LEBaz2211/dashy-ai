from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ai_service.prisma_models import Subtask, Task, Tag
from ai_service import schemas, models
from ai_service.prisma_models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Fetch tasks based on their IDs
def get_tasks_for_tagging(db: Session, task_ids: List[int]):
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()
    return tasks

# Update task tags
def update_task_tags(db: Session, task_id: int, tags: List[str]):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        # Clear existing tags
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

    # Fetch tasks based on their IDs
def get_tasks_for_subtasking(db: Session, task_ids: List[int]):
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()
    return tasks

def update_task_subtasks(db: Session, task_id: int, subtask_titles: List[str]):
    # Find the task for which subtasks need to be updated
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

    # Remove existing subtasks to replace them with the new list
    existing_subtasks = db.query(Subtask).filter(Subtask.taskId == task_id).all()
    for subtask in existing_subtasks:
        db.delete(subtask)

    # Add new subtasks provided in the list
    for title in subtask_titles:
        new_subtask = Subtask(title=title, task=task)
        db.add(new_subtask)

    db.commit()  # Commit changes to the database
    return task  # Return the task with updated subtasks

from typing import List
from sqlalchemy.orm import Session
from ai_service.prisma_models import User, Dashboard, TaskList, Task, Tag, Subtask

# User CRUD operations
def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()

def update_user(db: Session, user_id: str, user: schemas.UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Dashboard CRUD operations
def create_dashboard(db: Session, dashboard: schemas.DashboardCreate):
    db_dashboard = Dashboard(**dashboard.dict())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

def get_dashboard(db: Session, dashboard_id: int):
    return db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()

def delete_dashboard(db: Session, dashboard_id: int):
    db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    db.delete(db_dashboard)
    db.commit()

def update_dashboard(db: Session, dashboard_id: int, dashboard: schemas.DashboardCreate):
    db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if db_dashboard:
        for key, value in dashboard.dict().items():
            setattr(db_dashboard, key, value)
        db.commit()
        db.refresh(db_dashboard)
    return db_dashboard

# TaskList CRUD operations
def create_tasklist(db: Session, tasklist: schemas.TaskListCreate):
    db_tasklist = TaskList(**tasklist.dict())
    db.add(db_tasklist)
    db.commit()
    db.refresh(db_tasklist)
    return db_tasklist

def get_tasklist(db: Session, tasklist_id: int):
    return db.query(TaskList).filter(TaskList.id == tasklist_id).first()

def delete_tasklist(db: Session, tasklist_id: int):
    db_tasklist = db.query(TaskList).filter(TaskList.id == tasklist_id).first()
    
    if not db_tasklist:
        raise HTTPException(status_code=404, detail="TaskList not found")

    # Fetch all tasks associated with the task list
    tasks = db.query(Task).filter(Task.taskListId == tasklist_id).all()
    
    # Delete each task associated with the task list
    for task in tasks:
        db.delete(task)
    
    # Commit the deletions
    db.commit()

    # Now delete the task list itself
    db.delete(db_tasklist)
    db.commit()

    return db_tasklist



def update_tasklist(db: Session, tasklist_id: int, tasklist: schemas.TaskListCreate):
    db_tasklist = db.query(TaskList).filter(TaskList.id == tasklist_id).first()
    if db_tasklist:
        for key, value in tasklist.dict().items():
            setattr(db_tasklist, key, value)
        db.commit()
        db.refresh(db_tasklist)
    return db_tasklist

# Task CRUD operations
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(db_task)
    db.commit()

def update_task(db: Session, task_id: int, task: schemas.TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

# Tag CRUD operations
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    db.delete(db_tag)
    db.commit()

def update_tag(db: Session, tag_id: int, tag: schemas.TagCreate):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag:
        for key, value in tag.dict().items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag

# Subtask CRUD operations
def create_subtask(db: Session, subtask: schemas.SubtaskCreate):
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

def update_subtask(db: Session, subtask_id: int, subtask: schemas.SubtaskCreate):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if db_subtask:
        for key, value in subtask.dict().items():
            setattr(db_subtask, key, value)
        db.commit()
        db.refresh(db_subtask)
    return db_subtask


# Feedback CRUD operations
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# Fetch tasks based on their IDs
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task_update.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

# Subtask CRUD operations
def create_subtask(db: Session, subtask: schemas.SubtaskCreate):
    db_subtask = Subtask(**subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

def update_subtask(db: Session, subtask_id: int, subtask_update: schemas.SubtaskUpdate):
    db_subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if db_subtask:
        for key, value in subtask_update.dict().items():
            setattr(db_subtask, key, value)
        db.commit()
        db.refresh(db_subtask)
    return db_subtask

# Tag CRUD operations
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag

# AI Task CRUD operations
def get_ai_tasks_by_task_id(db: Session, task_id: int):
    return db.query(models.AITask).filter(models.AITask.related_task_id.contains(str(task_id))).all()

def search_tasks(db: Session, search_params: schemas.TaskSearch):
    query = db.query(Task)

    if search_params.title:
        query = query.filter(Task.title.contains(search_params.title))
    if search_params.tag:
        query = query.join(Task.tags).filter(Tag.name == search_params.tag)
    if search_params.due_date_from:
        query = query.filter(Task.dueDate >= search_params.due_date_from)
    if search_params.due_date_to:
        query = query.filter(Task.dueDate <= search_params.due_date_to)
    if search_params.completed is not None:
        query = query.filter(Task.completed == search_params.completed)

    return query.all()
