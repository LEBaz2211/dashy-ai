from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from ai_service import schemas, prisma_crud, crud
from ai_service.database import SessionLocalAI, SessionLocalPrisma
from ai_service.tagging import AutoTagging
from ai_service.feedback import FeedbackManager
from ai_service.models import Base as BaseAI
from ai_service.prisma_models import Base as BasePrisma

app = FastAPI()

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