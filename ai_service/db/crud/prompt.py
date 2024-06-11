from sqlalchemy.orm import Session
from ai_service.db import ai_models
from ai_service.db.schemas import PersonalizedPromptCreate

def create_personalized_prompt(db: Session, prompt: PersonalizedPromptCreate):
    db_prompt = ai_models.PersonalizedPrompt(**prompt.model_dump())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_personalized_prompts(db: Session, user_id: str):
    return db.query(ai_models.PersonalizedPrompt).filter_by(user_id=user_id).order_by(ai_models.PersonalizedPrompt.timestamp).all()
