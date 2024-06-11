from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, prisma_crud
from ai_service.db.database import get_db_prisma

router = APIRouter()

@router.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_tag(db, tag)

@router.get("/tags/{tag_id}", response_model=schemas.Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/tags/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    prisma_crud.delete_tag(db, tag_id)
    return db_tag

@router.put("/tags/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return prisma_crud.update_tag(db, tag_id, tag)
