from sqlalchemy.orm import Session
from ai_service.db import ai_models
from ai_service.db.schemas import ConversationCreate

def create_conversation(db: Session, conversation_create: ConversationCreate):
    conversation = ai_models.Conversation(**conversation_create.dict())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: int):
    return db.query(ai_models.Conversation).filter(ai_models.Conversation.id == conversation_id).first()

def update_conversation(db: Session, conversation_id: int, conversation_update: ConversationCreate):
    conversation = db.query(ai_models.Conversation).filter(ai_models.Conversation.id == conversation_id).first()
    if conversation:
        for key, value in conversation_update.dict().items():
            setattr(conversation, key, value)
        db.commit()
        db.refresh(conversation)
    return conversation
