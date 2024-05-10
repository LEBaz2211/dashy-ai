from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from .database import BaseAI as Base
import enum

class KnowledgeType(str, enum.Enum):
    project = 'project'
    object = 'object'
    course = 'course'
    preference = 'preference'
    other = 'other'

class PromptType(str, enum.Enum):
    auto_tag = 'auto_tag'
    auto_subtask = 'auto_subtask'
    auto_ranking = 'auto_ranking'
    general = 'general'

class TaskType(str, enum.Enum):
    auto_subtask = 'auto_subtask'
    auto_tag = 'auto_tag'
    auto_ranking = 'auto_ranking'
    general_assistance = 'general_assistance'

class AITask(Base):
    __tablename__ = 'ai_task'
    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(Enum(TaskType), nullable=False)
    related_task_id = Column(String(255), nullable=True)   # Foreign key to task table if applicable
    user_id = Column(String(255), index=True)
    ai_output = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())

class UserKnowledge(Base):
    __tablename__ = 'user_knowledge'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    type = Column(Enum(KnowledgeType), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ConversationMessage(Base):
    __tablename__ = 'conversation_message'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    role = Column(String(10), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=func.now())

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(50), nullable=False)  # Add this line
    ai_task_id = Column(Integer, ForeignKey('ai_task.id'), nullable=True)  # Now optional
    user_id = Column(String(255), index=True)
    feedback = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # Optional rating (1-5)
    timestamp = Column(DateTime, default=func.now())
    ai_task = relationship('AITask', back_populates='feedback', uselist=False)

AITask.feedback = relationship('Feedback', order_by=Feedback.id, back_populates='ai_task', uselist=False)


class PersonalizedPrompt(Base):
    __tablename__ = 'personalized_prompt'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    prompt = Column(Text, nullable=False)
    type = Column(Enum(PromptType), nullable=False)
    timestamp = Column(DateTime, default=func.now())
