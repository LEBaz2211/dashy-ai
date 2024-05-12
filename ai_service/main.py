from datetime import datetime
import json
from fastapi import FastAPI, HTTPException, Depends, Request, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ai_service import ai_manager, schemas, prisma_crud, crud
from ai_service.database import SessionLocalAI, SessionLocalPrisma
from ai_service.tagging import AutoTagging
from ai_service.feedback import FeedbackManager
from ai_service.models import Base as BaseAI
from ai_service.prisma_models import Base as BasePrisma


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For debugging, allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency for AI Database
def get_db_ai():
    db = SessionLocalAI()
    try:
        yield db
    finally:
        db.close()

# Dependency for Prisma Database
def get_db_prisma():
    db = SessionLocalPrisma()
    try:
        yield db
    finally:
        db.close()


@app.post("/auto_tag/", response_model=schemas.AutoTagResponse)
def auto_tag_tasks(auto_tag_request: schemas.AutoTagRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = prisma_crud.get_tasks_for_tagging(db_prisma, task_ids=auto_tag_request.tasks)

    print(tasks)

    tasks_to_tag = [
        {"id": task.id, "title": task.title}
        for task in tasks
    ]

    if not tasks_to_tag:
        raise HTTPException(status_code=404, detail="No tasks found for tagging")

    auto_tagger = AutoTagging(db_ai)
    tags_result, ai_task_id = auto_tagger.auto_tag_tasks(tasks_to_tag, auto_tag_request.user_id, auto_tag_request.tasks)

    updated_tasks = []
    for task_result in tags_result:
        task_id = task_result.get("id")
        tags = task_result.get("tags", [])
        prisma_crud.update_task_tags(db_prisma, task_id, tags)
        updated_tasks.append({"task_id": task_id, "tags": tags})

    return schemas.AutoTagResponse(updated_tasks=updated_tasks, ai_task_id=ai_task_id)

@app.post("/feedback/")
def create_feedback(feedback_request: schemas.FeedbackCreate, db: Session = Depends(get_db_ai)):
    feedback_manager = FeedbackManager(db)
    try:
        return feedback_manager.create_feedback(feedback_request)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content={"detail": exc.errors(), "body": await request.json()},
#     )

@app.post("/start_conversation/", response_model=schemas.Conversation)
async def start_conversation(conversation_create: schemas.ConversationCreate, db: Session = Depends(get_db_ai)):
    # try:
        manager = ai_manager.ConversationManager(db, conversation_create.user_id)
        conversation_data = manager.start_conversation(conversation_create.user_id, conversation_create.conversation)
        # print(conversation_data)
        conversation = crud.create_conversation(db, schemas.ConversationCreate(**conversation_data))
        return conversation
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))

@app.post("/continue_conversation/", response_model=schemas.Conversation)
def continue_conversation(conversation_data: schemas.ContinueConversation, db: Session = Depends(get_db_ai)):
    conversation = crud.get_conversation(db, conversation_data.conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    manager = ai_manager.ConversationManager(db, conversation.user_id)
    conversation_messages = manager.continue_conversation(conversation.conversation, conversation_data.user_message)

    conversation_data = {
        "user_id": conversation.user_id,
        "conversation": conversation_messages
    }
    updated_conversation = crud.update_conversation(db, conversation.id, schemas.ConversationCreate(**conversation_data))

    return updated_conversation
