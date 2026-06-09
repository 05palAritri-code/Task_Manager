from fastapi import APIRouter, Depends , status
import task_controller
from task_dtos import TaskSchema, TaskUpdateSchema
from sqlalchemy.orm import Session
from utils.db   import get_db

task_routes = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)
#------------------------------------------------------------------------------

@task_routes.post(
    "",
    summary="Create Task",
    description="Create a new task",
    status_code=status.HTTP_201_CREATED
)
def create_task(body: TaskSchema,db: Session=Depends(get_db)):

    return task_controller.create_task(body, db)
#------------------------------------------------------------------------------

@task_routes.get(
    "",
    summary="Get All Tasks",
    description="Retrieve all tasks",
    status_code=status.HTTP_200_OK
)
def get_all_tasks_route(db: Session=Depends(get_db)):

    return task_controller.get_all_tasks(db)

#------------------------------------------------------------------------------

@task_routes.put(
    "/{task_id}",
    summary="Update Task",
    description="Update a task",
    status_code=status.HTTP_201_CREATED
)
def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session = Depends(get_db)
):
    return task_controller.update_task(task_id, body, db)

#------------------------------------------------------------------------------

@task_routes.delete(
    "/{task_id}",
    summary="Delete Task",
    description="Delete a task",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    return task_controller.delete_task(task_id, db)
#------------------------------------------------------------------------------