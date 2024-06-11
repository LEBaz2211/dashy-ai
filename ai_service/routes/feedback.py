from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas
from ai_service.api.feedback import FeedbackManager
from ai_service.db.database import get_db_ai

router = APIRouter()

@router.post("/feedback/")
def create_feedback(feedback_request: schemas.FeedbackCreate, db: Session = Depends(get_db_ai)):
    feedback_manager = FeedbackManager(db)
    try:
        return feedback_manager.create_feedback(feedback_request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))