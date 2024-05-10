from sqlalchemy.orm import Session
from ai_service import schemas, crud
from ai_service.models import AITask

class FeedbackManager:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, feedback_data: schemas.FeedbackCreate):
        # Ensure `ai_task_id` exists in the `ai_task` table
        ai_task = self.db.query(AITask).filter(AITask.id == feedback_data.ai_task_id).first()
        if not ai_task:
            raise ValueError(f"AI Task with id {feedback_data.ai_task_id} not found")

        return crud.create_feedback(self.db, feedback_data)
