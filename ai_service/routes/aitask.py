from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, crud
from ai_service.db.database import get_db_ai

router = APIRouter()

@router.post("/aitasks/", response_model=schemas.AITask)
def create_aitask(ai_task: schemas.AITaskCreate, db: Session = Depends(get_db_ai)):
    return crud.create_ai_task(db, ai_task)

@router.get("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def get_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return db_ai_task

@router.delete("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def delete_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    crud.delete_ai_task(db, ai_task_id)
    return db_ai_task

@router.put("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def update_aitask(ai_task_id: int, ai_task: schemas.AITaskCreate, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return crud.update_ai_task(db, ai_task_id, ai_task)
