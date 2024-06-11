from typing import List, Optional
from fastapi import UploadFile
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

# class Task(BaseModel):
#     id: int
#     title: str

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

class AutoSubtaskRequest(BaseModel):
    tasks: List[int]
    user_id: str

class SubtaskUpdate(BaseModel):
    task_id: int
    subtasks: List[str]

class AutoSubtaskResponse(BaseModel):
    updated_tasks: List[SubtaskUpdate]
    ai_task_id: int

# Schemas for prisma_database
class UserBase(BaseModel):
    name: Optional[str]
    email: str

class UserCreate(UserBase):
    password: Optional[str] = None
    image: Optional[str] = None
    emailVerified: Optional[datetime] = None

class User(UserBase):
    id: str
    dashboards: List['Dashboard'] = []

    class Config:
        orm_mode = True

class DashboardBase(BaseModel):
    title: str
    userId: str

class DashboardCreate(DashboardBase):
    pass

class Dashboard(DashboardBase):
    id: int
    taskLists: List['TaskList'] = []

    class Config:
        orm_mode = True


class TaskListBase(BaseModel):
    title: str
    dashboardId: int

class TaskListCreate(TaskListBase):
    pass

class TaskList(TaskListBase):
    id: int
    tasks: List['Task'] = []

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    completed: Optional[bool] = False
    taskListId: int
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None

class TaskCreate(TaskBase):
    pass

# class Task(TaskBase):
#     id: int
#     completed: int
#     tags: List['Tag'] = []
#     subtasks: List['Subtask'] = []

#     class Config:
#         orm_mode = True

class SubtaskBase(BaseModel):
    title: str
    completed: Optional[bool] = False
    taskId: int

class SubtaskCreate(SubtaskBase):
    pass

class Subtask(SubtaskBase):
    id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class FeedbackCreate(BaseModel):
    task_type: str
    ai_task_id: int
    feedback: str
    rating: int

class Feedback(BaseModel):
    id: int
    task_type: str
    ai_task_id: int
    feedback: str
    rating: int
    timestamp: datetime

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None

class SubtaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = False
    taskId: int

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = False

class TagCreate(BaseModel):
    name: str

class Tag(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: int
    title: str
    completed: bool
    dueDate: Optional[datetime]
    reminder: Optional[datetime]
    notes: Optional[str]
    tags: List[Tag]
    subtasks: List[Subtask]

    class Config:
        orm_mode = True

class AITask(BaseModel):
    id: int
    task_type: str
    related_task_id: str
    user_id: str
    ai_output: str
    created_at: datetime

    class Config:
        orm_mode = True

class TaskSearchWithUser(BaseModel):
    user_id: str
    title: Optional[str] = None
    completed: Optional[bool] = None
    tag: Optional[str] = None

class TaskWithDetails(BaseModel):
    id: int
    title: str
    completed: bool
    taskListId: int
    dueDate: Optional[datetime] = None
    reminder: Optional[datetime] = None
    notes: Optional[str] = None
    task_list_title: str
    dashboard_title: str
    tags: List[str] = []
    subtasks: List[str] = []

    class Config:
        from_attributes = True

class UserCreateWithImage(BaseModel):
    name: Optional[str]
    email: str
    password: Optional[str] = None
    image: Optional[UploadFile] = None

class UserUpdateWithImage(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str] = None
    image: Optional[UploadFile] = None

class TagUpdate(BaseModel):
    task_id: int
    tags: List[str]

