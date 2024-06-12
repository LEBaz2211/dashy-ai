from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import TaskList, TaskListCreate
from ai_service.db.crud import (
    create_tasklist as crud_create_tasklist,
    get_tasklist as crud_get_tasklist,
    delete_tasklist as crud_delete_tasklist,
    update_tasklist as crud_update_tasklist,
)

router = APIRouter()

@router.post("/tasklists/", response_model=TaskList)
def create_tasklist_route(tasklist: TaskListCreate, db: Session = Depends(get_db_prisma)):
    return crud_create_tasklist(db, tasklist)

@router.get("/tasklists/{tasklist_id}", response_model=TaskList)
def get_tasklist_route(tasklist_id: int, db: Session = Depends(get_db_prisma)):
    db_tasklist = crud_get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return db_tasklist

@router.delete("/tasklists/{tasklist_id}", response_model=TaskList)
def delete_tasklist_route(tasklist_id: int, new_tasklist_id: int = None, db: Session = Depends(get_db_prisma)):
    if new_tasklist_id:
        return crud_delete_tasklist(db, tasklist_id, new_tasklist_id)
    else:
        return crud_delete_tasklist(db, tasklist_id)

@router.put("/tasklists/{tasklist_id}", response_model=TaskList)
def update_tasklist_route(tasklist_id: int, tasklist: TaskListCreate, db: Session = Depends(get_db_prisma)):
    db_tasklist = crud_get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return crud_update_tasklist(db, tasklist_id, tasklist)
