import json
from sqlalchemy.orm import Session
from . import models, schemas

# CRUD for AITask
def create_ai_task(db: Session, ai_task: schemas.AITaskCreate):
    db_ai_task = models.AITask(
        **ai_task.dict(exclude={"related_task_id"}),
        related_task_id=json.dumps(ai_task.related_task_id) if ai_task.related_task_id else None
    )
    db.add(db_ai_task)
    db.commit()
    db.refresh(db_ai_task)
    return db_ai_task

def get_ai_task(db: Session, ai_task_id: int):
    return db.query(models.AITask).filter(models.AITask.id == ai_task_id).first()

def get_ai_tasks_by_user(db: Session, user_id: str):
    return db.query(models.AITask).filter(models.AITask.user_id == user_id).all()

from sqlalchemy.orm import Session
from . import models, schemas

# CRUD for Feedback (Updated)
def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback(db: Session, task_type: str):
    return db.query(models.Feedback).filter_by(task_type=task_type).order_by(models.Feedback.timestamp).all()


# CRUD for UserKnowledge
def create_user_knowledge(db: Session, knowledge: schemas.UserKnowledgeCreate):
    db_knowledge = models.UserKnowledge(**knowledge.model_dump())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def get_user_knowledge(db: Session, user_id: str, knowledge_type: schemas.KnowledgeType):
    return db.query(models.UserKnowledge).filter_by(user_id=user_id, type=knowledge_type).all()

# CRUD for ConversationMessage
def create_conversation_message(db: Session, message: schemas.ConversationMessageCreate):
    db_message = models.ConversationMessage(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_conversation_history(db: Session, user_id: str):
    return db.query(models.ConversationMessage).filter_by(user_id=user_id).order_by(models.ConversationMessage.timestamp).all()

# CRUD for PersonalizedPrompt
def create_personalized_prompt(db: Session, prompt: schemas.PersonalizedPromptCreate):
    db_prompt = models.PersonalizedPrompt(**prompt.model_dump())
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

def get_personalized_prompts(db: Session, user_id: str):
    return db.query(models.PersonalizedPrompt).filter_by(user_id=user_id).order_by(models.PersonalizedPrompt.timestamp).all()
