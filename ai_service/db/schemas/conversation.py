from typing import List
from pydantic import BaseModel
from datetime import datetime

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
