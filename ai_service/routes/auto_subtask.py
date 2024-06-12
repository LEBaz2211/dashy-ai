from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.api.subtasks import AutoSubtasking
from ai_service.db.database import get_db_prisma, get_db_ai
from ai_service.db.schemas import AutoSubtaskRequest, AutoSubtaskResponse
from ai_service.db.crud import (
    get_tasks_for_subtasking as crud_get_tasks_for_subtasking,
    update_task_subtasks as crud_update_task_subtasks
)

router = APIRouter()

@router.post("/auto_subtask/", response_model=AutoSubtaskResponse)
def auto_subtask_tasks_route(auto_subtask_request: AutoSubtaskRequest, db_prisma: Session = Depends(get_db_prisma), db_ai: Session = Depends(get_db_ai)):
    tasks = crud_get_tasks_for_subtasking(db_prisma, task_ids=auto_subtask_request.tasks)

    tasks_to_subtask = [{"id": task.id, "title": task.title} for task in tasks]

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for subtasking")

    auto_subtasker = AutoSubtasking(db_ai)
    subtasks_result, ai_task_id = auto_subtasker.auto_subtask_tasks(tasks_to_subtask, auto_subtask_request.user_id, auto_subtask_request.tasks)

    updated_tasks = []
    for task_result in subtasks_result:
        task_id = task_result.get("id")
        subtasks = task_result.get("subtasks", [])
        crud_update_task_subtasks(db_prisma, task_id, subtasks)
        updated_tasks.append({"task_id": task_id, "subtasks": subtasks})

    return AutoSubtaskResponse(updated_tasks=updated_tasks, ai_task_id=ai_task_id)
