from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ai_service import prisma_models
from ai_service.prisma_models import Dashboard, Subtask, Task, Tag, TaskList
from ai_service import schemas, models
from ai_service.prisma_models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreateWithImage):
    db_user = prisma_models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        image=user.image.file.read() if user.image else None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: schemas.UserUpdateWithImage):
    db_user = db.query(prisma_models.User).filter(prisma_models.User.id == user_id).first()
    if db_user:
        if user.name is not None:
            db_user.name = user.name
        if user.email is not None:
            db_user.email = user.email
        if user.password is not None:
            db_user.password = user.password
        if user.image is not None:
            db_user.image = user.image.file.read()
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user_image(db: Session, user_id: str):
    return db.query(prisma_models.User).filter(prisma_models.User.id == user_id).first().image

def delete_user_image(db: Session, user_id: str):
    user = db.query(prisma_models.User).filter(prisma_models.User.id == user_id).first()
    if user:
        user.image = None
        db.commit()
        db.refresh(user)
    return user


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



def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()

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

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise ValueError(f"No task found with ID {task_id}")

    # Only update the fields if they are provided in the request
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


# Tag CRUD operations
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = Tag(**tag.dict())
    # check if tag already exists
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        # use that tag
        db_tag = existing_tag
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag_to_task(db: Session, task_id: int, tag_name: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

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
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

# Fetch tasks based on their IDs
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

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

def search_tasks_with_user(db: Session, search_params: schemas.TaskSearchWithUser):
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


# Fetch a tag by name
def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()

# Add a tag to a task
def add_tag_to_task(db: Session, task_id: int, tag_name: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

    tag = get_tag_by_name(db, tag_name)
    if not tag:
        tag = Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)

    if tag not in task.tags:
        task.tags.append(tag)
        db.commit()
        db.refresh(task)

    return task

# Remove a tag from a task and delete the tag if it's not associated with other tasks
def remove_tag_from_task(db: Session, task_id: int, tag_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise ValueError(f"No tag found with ID {tag_id}")

    if tag in task.tags:
        task.tags.remove(tag)
        db.commit()

    # Check if the tag is associated with any other tasks
    other_tasks = db.query(Task).filter(Task.tags.any(Tag.id == tag_id)).all()
    if not other_tasks:
        db.delete(tag)
        db.commit()

    return task