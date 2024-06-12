from fastapi import APIRouter, Depends, HTTPException, UploadFile #, StreamingResponse
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from io import BytesIO
from ai_service.db import database
from ai_service.db.schemas import UserUpdateWithImage, User, UserCreate
from ai_service.db.crud import (
    create_user as crud_create_user,
    update_user as crud_update_user,
    get_user_image as crud_get_user_image,
    delete_user_image as crud_delete_user_image,
    get_user as crud_get_user,
    delete_user as crud_delete_user
)

router = APIRouter()

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(database.get_db_prisma)):
    return crud_create_user(db, user)

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, db: Session = Depends(database.get_db_prisma)):
    db_user = crud_get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    image: Optional[UploadFile] = None,
    db: Session = Depends(database.get_db_prisma)
):
    user_update = UserUpdateWithImage(name=name, email=email, password=password, image=image)
    db_user = crud_update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: str, db: Session = Depends(database.get_db_prisma)):
    db_user = crud_get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_delete_user(db, user_id)
    return db_user

@router.get("/users/{user_id}/image")
def get_user_image(user_id: str, db: Session = Depends(database.get_db_prisma)):
    image_data = crud_get_user_image(db, user_id)
    if not image_data:
        return {"message": "No image available for this user"}
    
    return StreamingResponse(
        content=BytesIO(image_data),
        media_type="image/jpeg"
    )

@router.delete("/users/{user_id}/image", response_model=User)
def delete_user_image(user_id: str, db: Session = Depends(database.get_db_prisma)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_delete_user_image(db, user_id)
    return user
