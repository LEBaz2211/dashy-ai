from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, crud
from ai_service.api.ai_manager import ConversationManager
from ai_service.db.database import get_db_ai

router = APIRouter()

@router.post("/start_conversation/", response_model=schemas.Conversation)
async def start_conversation(conversation_create: schemas.ConversationCreate, db: Session = Depends(get_db_ai)):
    manager = ConversationManager(db, conversation_create.user_id)
    conversation_data = manager.start_conversation(conversation_create.user_id, conversation_create.conversation)
    conversation = crud.create_conversation(db, schemas.ConversationCreate(**conversation_data))
    return conversation

@router.post("/continue_conversation/", response_model=schemas.Conversation)
def continue_conversation(conversation_data: schemas.ContinueConversation, db: Session = Depends(get_db_ai)):
    conversation = crud.get_conversation(db, conversation_data.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    manager = ConversationManager(db, conversation.user_id)
    conversation_messages = manager.continue_conversation(conversation.conversation, conversation_data.user_message)

    conversation_data = {"user_id": conversation.user_id, "conversation": conversation_messages}
    updated_conversation = crud.update_conversation(db, conversation.id, schemas.ConversationCreate(**conversation_data))

    return updated_conversation
