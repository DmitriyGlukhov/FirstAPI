from fastapi import Depends, HTTPException, Query, APIRouter
from starlette import status
from api_models import CreateTaskData, ResponseTaskData, ResponseTasks
from dependencies import auth_user, get_database
from db import DataBase, User, Task
from typing import List


router_task = APIRouter(prefix='/task', tags=['task'])

@router_task.post("/", summary="Создать задачу")
async def create_task(
        task_data: CreateTaskData,
        user: User = Depends(auth_user),
        db: DataBase = Depends(get_database)
):
    db.create_task(user_id=user.id, title=task_data.title, text=task_data.text, priority=task_data.priority, deadline=task_data.deadline)
    return {"status": "ok"}


@router_task.post("/{task_id}", summary="Изменить задачу")
async def change_task(
        task_data: CreateTaskData,
        task_id: int,
        user: User = Depends(auth_user),
        db: DataBase = Depends(get_database)
):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if task.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
    task.title = task_data.title
    task.text = task_data.text
    task.priority = task_data.priority
    task.deadline = task_data.deadline
    task.save()
    
    return {"status": "ok"}


@router_task.delete("/{task_id}")
async def delete_task(
    task_id: int,
    user: User = Depends(auth_user),
    db: DataBase = Depends(get_database)
):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if task.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    task.delete()
    
    return {"status": "ok"}


@router_task.get("/get_some", response_model=ResponseTasks)
async def get_tasks(
    time_from: int | None = Query(None, description="От времени"),
    time_to: int | None = Query(None, description="До времени"),
    priority: int | None = Query(None, ge=0, le=3, description="Приоритет"),
    user: User = Depends(auth_user),
    db: DataBase = Depends(get_database)
) -> List[dict]:
    tasks = user.get_tasks(priority=priority, time_from=time_from, time_to=time_to)

    return ResponseTasks.model_validate({'tasks': [ResponseTaskData.model_validate(t.get_fields()) for t in tasks]})

    
@router_task.get("/{task_id}")
async def get_task(
    task_id: int,
    user = Depends(auth_user),
    db = Depends(get_database)
):
    task = db.get_task(task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if task.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
    return ResponseTaskData.model_validate(task.get_fields())


