from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db.common_models import TaskList, Task
from ai_service.db.schemas import TaskListCreate

def create_tasklist(db: Session, tasklist: TaskListCreate):
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

    tasks = db.query(Task).filter(Task.taskListId == tasklist_id).all()
    for task in tasks:
        db.delete(task)
    db.commit()

    db.delete(db_tasklist)
    db.commit()

    return db_tasklist

def update_tasklist(db: Session, tasklist_id: int, tasklist: TaskListCreate):
    db_tasklist = db.query(TaskList).filter(TaskList.id == tasklist_id).first()
    if db_tasklist:
        for key, value in tasklist.dict().items():
            setattr(db_tasklist, key, value)
        db.commit()
        db.refresh(db_tasklist)
    return db_tasklist
