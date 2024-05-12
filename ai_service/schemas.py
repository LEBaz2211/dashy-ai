from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
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

class AITaskBase(BaseModel):
    task_type: TaskType
    related_task_id: Optional[List[int]] = None
    user_id: str
    ai_output: str

class AITaskCreate(AITaskBase):
    pass

class AITask(AITaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserKnowledgeBase(BaseModel):
    user_id: str
    type: KnowledgeType
    content: str

class UserKnowledgeCreate(UserKnowledgeBase):
    pass

class UserKnowledge(UserKnowledgeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ConversationMessageBase(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ConversationMessage(ConversationMessageBase):
    timestamp: datetime

    class Config:
        orm_mode = True

class ConversationCreate(BaseModel):
    user_id: str
    conversation: List[ConversationMessageBase]

class Conversation(BaseModel):
    id: int
    user_id: str
    conversation: List[ConversationMessageBase]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ContinueConversation(BaseModel):
    conversation_id: int
    user_message: str

class FeedbackBase(BaseModel):
    task_type: TaskType
    ai_task_id: int
    user_id: str
    feedback: str
    rating: Optional[int] = None  # Optional rating (1-5)

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class PersonalizedPromptBase(BaseModel):
    user_id: str
    prompt: str
    type: PromptType

class PersonalizedPromptCreate(PersonalizedPromptBase):
    pass

class PersonalizedPrompt(PersonalizedPromptBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: int
    title: str

class DashboardTestRequest(BaseModel):
    user_id: str
    dashboard_id: int

class TaskListTestRequest(BaseModel):
    dashboard_id: int
    task_list_id: int

class TaskTagUpdate(BaseModel):
    task_id: int
    tags: List[str]

class AutoTagRequest(BaseModel):
    tasks: List[int]
    user_id: str

class AutoTagResponse(BaseModel):
    updated_tasks: List[TaskTagUpdate]
    ai_task_id: int
