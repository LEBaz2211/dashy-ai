from datetime import datetime, timedelta
from io import BytesIO
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ai_service.db import schemas
from ai_service.api import ai_manager
from ai_service.db import crud, prisma_crud
from .db import crud, database, schemas
from .api import auth
from ai_service.db.database import SessionLocalAI, SessionLocalPrisma
from ai_service.api.subtasks import AutoSubtasking
from ai_service.api.tagging import AutoTagging
from ai_service.api.feedback import FeedbackManager
from ai_service.db.models import Base as BaseAI
from ai_service.db.prisma_models import Base as BasePrisma, Subtask, Tag, Task
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ai_service.db.database import get_db_ai, get_db_prisma
from .routes import task_endpoints
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from fastapi.responses import StreamingResponse


app = FastAPI()

app.include_router(auth.router)
app.include_router(task_endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auto_tag/", response_model=schemas.AutoTagResponse)
def auto_tag_tasks(auto_tag_request: schemas.AutoTagRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = prisma_crud.get_tasks_for_tagging(db_prisma, task_ids=auto_tag_request.tasks)

    # print(tasks)

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

@app.post("/auto_subtask/", response_model=schemas.AutoSubtaskResponse)
def auto_subtask_tasks(auto_subtask_request: schemas.AutoSubtaskRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = prisma_crud.get_tasks_for_subtasking(db_prisma, task_ids=auto_subtask_request.tasks)

    print(tasks)

    tasks_to_subtask = [
        {"id": task.id, "title": task.title}
        for task in tasks
    ]

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for subtasking")

    auto_subtasker = AutoSubtasking(db_ai)
    subtasks_result, ai_task_id = auto_subtasker.auto_subtask_tasks(tasks_to_subtask, auto_subtask_request.user_id, auto_subtask_request.tasks)

    updated_tasks = []
    for task_result in subtasks_result:
        task_id = task_result.get("id")
        subtasks = task_result.get("subtasks", [])
        prisma_crud.update_task_subtasks(db_prisma, task_id, subtasks)
        updated_tasks.append({"task_id": task_id, "subtasks": subtasks})

    return schemas.AutoSubtaskResponse(updated_tasks=updated_tasks, ai_task_id=ai_task_id)




# AITask Endpoints
@app.post("/aitasks/", response_model=schemas.AITask)
def create_aitask(ai_task: schemas.AITaskCreate, db: Session = Depends(get_db_ai)):
    return crud.create_ai_task(db, ai_task)

@app.get("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def get_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return db_ai_task

@app.delete("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def delete_aitask(ai_task_id: int, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    crud.delete_ai_task(db, ai_task_id)
    return db_ai_task

@app.put("/aitasks/{ai_task_id}", response_model=schemas.AITask)
def update_aitask(ai_task_id: int, ai_task: schemas.AITaskCreate, db: Session = Depends(get_db_ai)):
    db_ai_task = crud.get_ai_task(db, ai_task_id)
    if db_ai_task is None:
        raise HTTPException(status_code=404, detail="AITask not found")
    return crud.update_ai_task(db, ai_task_id, ai_task)

# @app.get("/aitasks/user/{user_id}", response_model=List[schemas.AITask])
# def get_aitasks_by_user(user_id: str, db: Session = Depends(get_db_ai)):
#     return crud.get_ai_tasks_by_user(db, user_id)

# User Endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db_prisma)):
    db_user = prisma_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
    image: Optional[UploadFile] = None,
    db: Session = Depends(database.get_db_prisma)
):
    user_update = schemas.UserUpdateWithImage(name=name, email=email, password=password, image=image)
    db_user = prisma_crud.update_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: str, db: Session = Depends(database.get_db_prisma)):
    db_user = prisma_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    prisma_crud.delete_user(db, user_id)
    return db_user

@app.get("/users/{user_id}/image")
def get_user_image(user_id: str, db: Session = Depends(database.get_db_prisma)):
    image_data = prisma_crud.get_user_image(db, user_id)
    if not image_data:
        # Return a default response or a message indicating no image
        return {"message": "No image available for this user"}
    
    return StreamingResponse(
        content=BytesIO(image_data),
        media_type="image/jpeg"
    )


@app.delete("/users/{user_id}/image", response_model=schemas.User)
def delete_user_image(user_id: str, db: Session = Depends(database.get_db_prisma)):
    user = prisma_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = prisma_crud.delete_user_image(db, user_id)
    return user

# Dashboard Endpoints
@app.post("/dashboards/", response_model=schemas.Dashboard)
def create_dashboard(dashboard: schemas.DashboardCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_dashboard(db, dashboard)

@app.get("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard

@app.delete("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    prisma_crud.delete_dashboard(db, dashboard_id)
    return db_dashboard

@app.put("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def update_dashboard(dashboard_id: int, dashboard: schemas.DashboardCreate, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return prisma_crud.update_dashboard(db, dashboard_id, dashboard)

# TaskList Endpoints
@app.post("/tasklists/", response_model=schemas.TaskList)
def create_tasklist(tasklist: schemas.TaskListCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_tasklist(db, tasklist)

@app.get("/tasklists/{tasklist_id}", response_model=schemas.TaskList)
def get_tasklist(tasklist_id: int, db: Session = Depends(get_db_prisma)):
    db_tasklist = prisma_crud.get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return db_tasklist

@app.delete("/tasklists/{tasklist_id}", response_model=schemas.TaskList)
def delete_tasklist(tasklist_id: int, new_tasklist_id: int = None, db: Session = Depends(get_db_prisma)):
    if new_tasklist_id:
        return prisma_crud.delete_tasklist(db, tasklist_id, new_tasklist_id)
    else:
        return prisma_crud.delete_tasklist(db, tasklist_id)

@app.put("/tasklists/{tasklist_id}", response_model=schemas.TaskList)
def update_tasklist(tasklist_id: int, tasklist: schemas.TaskListCreate, db: Session = Depends(get_db_prisma)):
    db_tasklist = prisma_crud.get_tasklist(db, tasklist_id)
    if db_tasklist is None:
        raise HTTPException(status_code=404, detail="TaskList not found")
    return prisma_crud.update_tasklist(db, tasklist_id, tasklist)

# Task Endpoints
# @app.post("/tasks/", response_model=schemas.Task)
# def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db_prisma)):
#     return prisma_crud.create_task(db, task)

# @app.get("/tasks/{task_id}", response_model=schemas.Task)
# def get_task(task_id: int, db: Session = Depends(get_db_prisma)):
#     db_task = prisma_crud.get_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task

# @app.delete("/tasks/{task_id}", response_model=schemas.Task)
# def delete_task(task_id: int, db: Session = Depends(get_db_prisma)):
#     db_task = prisma_crud.get_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     prisma_crud.delete_task(db, task_id)
#     return db_task

# @app.put("/tasks/{task_id}", response_model=schemas.Task)
# def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db_prisma)):
#     db_task = prisma_crud.get_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return prisma_crud.update_task(db, task_id, task)

# Tag Endpoints
@app.post("/tags/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_tag(db, tag)

@app.get("/tags/{tag_id}", response_model=schemas.Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@app.delete("/tags/{tag_id}", response_model=schemas.Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    prisma_crud.delete_tag(db, tag_id)
    return db_tag

@app.put("/tags/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db_prisma)):
    db_tag = prisma_crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return prisma_crud.update_tag(db, tag_id, tag)

# Subtask Endpoints
@app.post("/subtasks/", response_model=schemas.Subtask)
def create_subtask(subtask: schemas.SubtaskCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_subtask(db, subtask)

@app.get("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def get_subtask(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return db_subtask

@app.delete("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def delete_subtask(subtask_id: int, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    prisma_crud.delete_subtask(db, subtask_id)
    return db_subtask

@app.put("/subtasks/{subtask_id}", response_model=schemas.Subtask)
def update_subtask(subtask_id: int, subtask: schemas.SubtaskCreate, db: Session = Depends(get_db_prisma)):
    db_subtask = prisma_crud.get_subtask(db, subtask_id)
    if db_subtask is None:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return prisma_crud.update_subtask(db, subtask_id, subtask)

