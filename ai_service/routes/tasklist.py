from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import prisma_crud
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import TaskList, TaskListCreate

router = APIRouter()

@router.post("/tasklists/", response_model=TaskList)
def create_tasklist(tasklist: TaskListCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_tasklist(db, tasklist)

@router.get("/tasklists/{tasklist_id}", response_model=TaskList)
def get_tasklist(tasklist_id: int, db: Session = Depends(get_db_prisma)):
    db_tasklist = prisma_crud.get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return db_tasklist

@router.delete("/tasklists/{tasklist_id}", response_model=TaskList)
def delete_tasklist(tasklist_id: int, new_tasklist_id: int = None, db: Session = Depends(get_db_prisma)):
    if new_tasklist_id:
        return prisma_crud.delete_tasklist(db, tasklist_id, new_tasklist_id)
    else:
        return prisma_crud.delete_tasklist(db, tasklist_id)

@router.put("/tasklists/{tasklist_id}", response_model=TaskList)
def update_tasklist(tasklist_id: int, tasklist: TaskListCreate, db: Session = Depends(get_db_prisma)):
    db_tasklist = prisma_crud.get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return prisma_crud.update_tasklist(db, tasklist_id, tasklist)
