from typing import List
from sqlalchemy.orm import Session
from ai_service.prisma_models import Task, Tag

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
