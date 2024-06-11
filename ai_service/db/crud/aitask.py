import json
from sqlalchemy.orm import Session
from ai_service.db import ai_models
from ai_service.db.schemas import AITaskCreate

def create_ai_task(db: Session, ai_task: AITaskCreate):
    db_ai_task = ai_models.AITask(
        **ai_task.dict(exclude={"related_task_id"}),
        related_task_id=json.dumps(ai_task.related_task_id) if ai_task.related_task_id else None
    )
    db.add(db_ai_task)
    db.commit()
    db.refresh(db_ai_task)
    return db_ai_task

def get_ai_task(db: Session, ai_task_id: int):
    return db.query(ai_models.AITask).filter(ai_models.AITask.id == ai_task_id).first()

def get_ai_tasks_by_user(db: Session, user_id: str):
    return db.query(ai_models.AITask).filter(ai_models.AITask.user_id == user_id).all()

def get_ai_tasks_by_task_id(db: Session, task_id: int):
    return db.query(ai_models.AITask).filter(ai_models.AITask.related_task_id.contains([task_id])).all()
