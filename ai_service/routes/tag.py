from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import TagCreate, Tag
from ai_service.db.crud import (
    create_tag as crud_create_tag,
    get_tag as crud_get_tag,
    delete_tag as crud_delete_tag,
    update_tag as crud_update_tag
)

router = APIRouter()

@router.post("/tags/", response_model=Tag)
def create_tag_route(tag: TagCreate, db: Session = Depends(get_db_prisma)):
    return crud_create_tag(db, tag)

@router.get("/tags/{tag_id}", response_model=Tag)
def get_tag_route(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = crud_get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/tags/{tag_id}", response_model=Tag)
def delete_tag_route(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = crud_get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    crud_delete_tag(db, tag_id)
    return db_tag

@router.put("/tags/{tag_id}", response_model=Tag)
def update_tag_route(tag_id: int, tag: TagCreate, db: Session = Depends(get_db_prisma)):
    db_tag = crud_get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return crud_update_tag(db, tag_id, tag)
