from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, prisma_crud
from ai_service.db.database import get_db_prisma

router = APIRouter()

@router.post("/subtasks/", response_model=schemas.Subtask)
def create_subtask(subtask: schemas.SubtaskCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_subtask(db, subtask)

@router.get("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def get_subtask(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return db_subtask

@router.delete("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def delete_subtask(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    prisma_crud.delete_subtask(db, subtask_id)
    return db_subtask

@router.put("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def update_subtask(subtask_id: int, subtask: schemas.SubtaskCreate, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return prisma_crud.update_subtask(db, subtask_id, subtask)
