from sqlalchemy.orm import Session
from ai_service.db.ai_models import Feedback
from ai_service.db.schemas import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session, task_type: str):
    return db.query(Feedback).filter_by(task_type=task_type).order_by(Feedback.timestamp).all()
