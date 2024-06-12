from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import SubtaskCreate, Subtask, SubtaskUpdate
from ai_service.db.crud import (
    create_subtask as crud_create_subtask,
    get_subtask as crud_get_subtask,
    delete_subtask as crud_delete_subtask,
    update_subtask as crud_update_subtask,
)

router = APIRouter()

@router.post("/subtasks/", response_model=Subtask)
def create_subtask_route(subtask: SubtaskCreate, db: Session = Depends(get_db_prisma)):
    return crud_create_subtask(db, subtask)

@router.get("/subtasks/{subtask_id}", response_model=Subtask)
def get_subtask_route(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = crud_get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return db_subtask

@router.delete("/subtasks/{subtask_id}", response_model=Subtask)
def delete_subtask_route(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = crud_get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    crud_delete_subtask(db, subtask_id)
    return db_subtask

@router.put("/subtasks/{subtask_id}", response_model=Subtask)
def update_subtask_route(subtask_id: int, subtask: SubtaskCreate, db: Session = Depends(get_db_prisma)):
    db_subtask = crud_get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return crud_update_subtask(db, subtask_id, subtask)
