from datetime import datetime, time, timedelta, timezone


from sqlalchemy.orm import Session
from app.db.models import Category, Task
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



def post_task(db , user_id ,task : TaskCreate):


    # While creating a task it will prevent a db crash and handle task existance  if task does not exist it will return status_code =  404 instead of 500
    if task.category_id is not None:
        found_category = db.query(Category).filter(
            Category.id == task.category_id,
            Category.user_id == user_id 
        ).first()

        if not found_category:
            raise HTTPException(status_code=404,detail="Category not found")



    new_task = Task(
        title = task.title,
        description = task.description,
        is_complete = task.is_complete,
        category_id = task.category_id,
        due_date = task.due_date,
        user_id = user_id

    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks_due_today(db : Session, user_id):
    

    # Get current datetime with timezone 
    now = datetime.now(timezone.utc)

    # Sets start time for today
    start_today = datetime.combine(
        now.date(),
        time.min,
        tzinfo=timezone.utc
    )

    # Sets start time for tomorrow 
    start_tomorrow = start_today + timedelta(days=1)



    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date >= start_today,
        Task.due_date < start_tomorrow

    ).order_by(Task.due_date.asc()) # orders by due_data ascending order 
    
    return tasks.all()


