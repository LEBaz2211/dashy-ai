from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import crud
from ai_service.db.database import get_db_ai
from ai_service.db.schemas import AITask, AITaskCreate

router = APIRouter()

@router.post("/aitasks/", response_model=AITask)
def create_aitask(ai_task: AITaskCreate, db: Session = Depends(get_db_ai)):
    return crud.create_ai_task(db, ai_task)

@router.get("/aitasks/{ai_task_id}", response_model=AITask)
def get_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return db_ai_task

@router.delete("/aitasks/{ai_task_id}", response_model=AITask)
def delete_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    crud.delete_ai_task(db, ai_task_id)
    return db_ai_task

@router.put("/aitasks/{ai_task_id}", response_model=AITask)
def update_aitask(ai_task_id: int, ai_task: AITaskCreate, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return crud.update_ai_task(db, ai_task_id, ai_task)
