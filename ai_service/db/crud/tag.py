from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db.common_models import Tag, Task
from ai_service.db.schemas import TagCreate

def create_tag(db: Session, tag: TagCreate):
    db_tag = Tag(**tag.dict())
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        db_tag = existing_tag
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

def update_tag(db: Session, tag_id: int, tag: TagCreate):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if db_tag:
        for key, value in tag.dict().items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag

def add_tag_to_task(db: Session, task_id: int, tag_name: str):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError(f"No task found with ID {task_id}")

    tag = db.query(Tag).filter(Tag.name == tag_name).first()
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

    other_tasks = db.query(Task).filter(Task.tags.any(Tag.id == tag_id)).all()
    if not other_tasks:
        db.delete(tag)
        db.commit()

    return task
