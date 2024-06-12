from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db import common_models
from ai_service.db.schemas import UserCreateWithImage, UserUpdateWithImage
from ai_service.db.common_models import User

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreateWithImage):
    db_user = common_models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        image=user.image.file.read() if user.image else None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user: UserUpdateWithImage):
    db_user = db.query(common_models.User).filter(common_models.User.id == user_id).first()
    if db_user:
        if user.name is not None:
            db_user.name = user.name
        if user.email is not None:
            db_user.email = user.email
        if user.password is not None:
            db_user.password = user.password
        if user.image is not None:
            db_user.image = user.image.file.read()
        db.commit()
        db.refresh(db_user)
    return db_user

def get_user_image(db: Session, user_id: str):
    return db.query(common_models.User).filter(common_models.User.id == user_id).first().image

def delete_user_image(db: Session, user_id: str):
    user = db.query(common_models.User).filter(common_models.User.id == user_id).first()
    if user:
        user.image = None
        db.commit()
        db.refresh(user)
    return user

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
