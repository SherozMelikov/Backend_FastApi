from datetime import datetime

from sqlalchemy.orm import Session
from app.db.models import Task
from fastapi.exceptions import HTTPException

from app.schemas.tasks import TaskCreate, TaskUpdate

def get_tasks_for_user(db : Session , user_id):
    tasks = db.query(Task).filter(Task.user_id==user_id).all()

    return tasks

def get_task_for_user(db: Session , user_id, task_id):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
        
    ).first()
    if task is None :
        raise HTTPException(status_code=404, detail="Task not found") 

    return task

def put_task(
    db: Session,
    user_id: int,
    task_id: int,
    task: TaskUpdate,
):
    found_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id,
    ).first()

    if found_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "is_complete":
            found_task.is_complete = value

            if value is True:
                found_task.completed_at = datetime.utcnow()
            else:
                found_task.completed_at = None
        else:
            setattr(found_task, field, value)

    db.commit()
    db.refresh(found_task)

    return found_task

def delete_task(db, user_id , task_id):
    found_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id 
    ).first()

    if not found_task:
        raise HTTPException(status_code=404,detail="Task not found")
    
    db.delete(found_task)
    db.commit()

    return {"message": "Task is successfully deleted !"}



def post_task(db , user_id ,task : TaskCreate ):
    new_task = Task(
        title = task.title,
        description = task.description,
        is_complete = task.is_complete,
        user_id = user_id

    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

