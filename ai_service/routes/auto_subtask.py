from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, prisma_crud
from ai_service.api.subtasks import AutoSubtasking
from ai_service.db.database import get_db_prisma, get_db_ai

router = APIRouter()

@router.post("/auto_subtask/", response_model=schemas.AutoSubtaskResponse)
def auto_subtask_tasks(auto_subtask_request: schemas.AutoSubtaskRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = prisma_crud.get_tasks_for_subtasking(db_prisma, task_ids=auto_subtask_request.tasks)

    tasks_to_subtask = [{"id": task.id, "title": task.title} for task in tasks]

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
