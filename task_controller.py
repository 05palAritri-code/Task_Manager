from task_dtos import TaskSchema,TaskUpdateSchema
from sqlalchemy.orm import Session
from tables import TaskModel

#------------------------------------------------------------------------------

def create_task(body : TaskSchema, db : Session):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"], 
                         description = data["description"], 
                         status = data["status"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully"}

#------------------------------------------------------------------------------

def get_all_tasks(db : Session):

    tasks = db.query(TaskModel).all()

    return {"status": "All Task" , "data": tasks}

from fastapi import HTTPException

#------------------------------------------------------------------------------

def get_task(task_id: int, db: Session):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task fetched successfully",
        "data": task
    }

#------------------------------------------------------------------------------

def update_task(
    task_id: int,
    body: TaskUpdateSchema,
    db: Session
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    data = body.model_dump()

    task.title = data["title"]
    task.description = data["description"]
    task.status = data["status"]

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "data": task
    }

#------------------------------------------------------------------------------

def delete_task(
    task_id: int,
    db: Session
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return None