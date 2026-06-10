from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import task_controller

from task_dtos import TaskSchema, TaskUpdateSchema
from utils.db import get_db
from utils.security import get_current_user

task_routes = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)
#------------------------------------------------------------------------------

@task_routes.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_task(
    body: TaskSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return task_controller.create_task(
        body,
        db,
        user
    )
#------------------------------------------------------------------------------

@task_routes.get(
    "",
    status_code=status.HTTP_200_OK
)
def get_all_tasks_route(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return task_controller.get_all_tasks(
        db,
        user
    )

#------------------------------------------------------------------------------
@task_routes.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return task_controller.get_task(
        task_id,
        db,
        user
    )
#------------------------------------------------------------------------------

@task_routes.put(
    "/{task_id}",
    status_code=status.HTTP_200_OK
)
def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return task_controller.update_task(
        task_id,
        body,
        db,
        user
    )
#------------------------------------------------------------------------------

@task_routes.delete(
    "/{task_id}",
    status_code=status.HTTP_200_OK
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return task_controller.delete_task(
        task_id,
        db,
        user
    )
#------------------------------------------------------------------------------