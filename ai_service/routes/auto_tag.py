from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.api.tagging import AutoTagging
from ai_service.db.database import get_db_prisma, get_db_ai
from ai_service.db.schemas import AutoTagRequest, AutoTagResponse
from ai_service.db.crud import (
    get_tasks_for_tagging as crud_get_tasks_for_tagging,
    update_task_tags as crud_update_task_tags
)

router = APIRouter()

@router.post("/auto_tag/", response_model=AutoTagResponse)
def auto_tag_tasks_route(auto_tag_request: AutoTagRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = crud_get_tasks_for_tagging(db_prisma, task_ids=auto_tag_request.tasks)

    tasks_to_tag = [{"id": task.id, "title": task.title} for task in tasks]

    if not tasks_to_tag:
        raise HTTPException(status_code=404, detail="No tasks found for tagging")

    auto_tagger = AutoTagging(db_ai)
    tags_result, ai_task_id = auto_tagger.auto_tag_tasks(tasks_to_tag, auto_tag_request.user_id, auto_tag_request.tasks)

    updated_tasks = []
    for task_result in tags_result:
        task_id = task_result.get("id")
        tags = task_result.get("tags", [])
        crud_update_task_tags(db_prisma, task_id, tags)
        updated_tasks.append({"task_id": task_id, "tags": tags})

    return AutoTagResponse(updated_tasks=updated_tasks, ai_task_id=ai_task_id)
