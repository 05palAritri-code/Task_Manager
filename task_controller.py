from task_dtos import TaskSchema,TaskUpdateSchema
from sqlalchemy.orm import Session
from tables import TaskModel
from fastapi import HTTPException,status,Request,Depends
from utils.security import get_current_user
from utils.db import get_db
#------------------------------------------------------------------------------
def create_task(
    body: TaskSchema,
    db: Session,
    user
):
    new_task = TaskModel(
        title=body.title,
        description=body.description,
        status=body.status,
        user_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "success": True,
        "message": "Task created successfully",
        "data": new_task
    }

def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.headers.get("authorization")

    print("AUTH HEADER =", token)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Unauthenticated"
        )
# ------------------------------------------------------------------------------
# GET ALL TASKS
# ------------------------------------------------------------------------------

def get_all_tasks(
    db: Session,
    user
):
    tasks = db.query(TaskModel).filter(
        TaskModel.user_id == user.id
    ).all()

    return {
        "success": True,
        "message": "Tasks fetched successfully",
        "data": tasks
    }


# ------------------------------------------------------------------------------
# GET SINGLE TASK
# ------------------------------------------------------------------------------

def get_task(
    task_id: int,
    db: Session,
    user
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return {
        "success": True,
        "message": "Task fetched successfully",
        "data": task
    }


# ------------------------------------------------------------------------------
# UPDATE TASK
# ------------------------------------------------------------------------------

def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session,
    user
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = body.title
    task.description = body.description
    task.status = body.status

    db.commit()
    db.refresh(task)

    return {
        "success": True,
        "message": "Task updated successfully",
        "data": task
    }


# ------------------------------------------------------------------------------
# DELETE TASK
# ------------------------------------------------------------------------------

def delete_task(
    task_id: int,
    db: Session,
    user
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "success": True,
        "message": "Task deleted successfully",
        "data": None
    }