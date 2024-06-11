from sqlalchemy.orm import Session
from ai_service.db import ai_models
from ai_service.db.schemas import UserKnowledgeCreate, KnowledgeType

def create_user_knowledge(db: Session, knowledge: UserKnowledgeCreate):
    db_knowledge = ai_models.UserKnowledge(**knowledge.model_dump())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def get_user_knowledge(db: Session, user_id: str, knowledge_type: KnowledgeType):
    return db.query(ai_models.UserKnowledge).filter_by(user_id=user_id, type=knowledge_type).all()
