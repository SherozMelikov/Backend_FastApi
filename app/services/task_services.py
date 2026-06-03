from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


from sqlalchemy.orm import Session
from app.db.models import Category, Task
from fastapi.exceptions import HTTPException

from app.schemas.tasks import TaskCreate, TaskUpdate
from app.utils.datetime_utils import utc_now

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
                found_task.completed_at = utc_now()
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

    # If category_id is provided, check that the category exists
    # and belongs to the current user before creating the task.

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
        user_id = user_id,
        priority = task.priority,
        impact_level = task.impact_level

    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_due_today(db: Session, user_id: int, user_timezone: str):
    
    
    try:
        user_tz = ZoneInfo(user_timezone)
    except Exception:
        user_tz = timezone.utc

    now_user_time = utc_now().astimezone(user_tz)

    start_today_user_time = datetime.combine(
        now_user_time.date(),
        time.min,
        tzinfo=user_tz
    )

    start_tomorrow_user_time = start_today_user_time + timedelta(days=1)

    start_today_utc = start_today_user_time.astimezone(timezone.utc)
    start_tomorrow_utc = start_tomorrow_user_time.astimezone(timezone.utc)

    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date >= start_today_utc,
        Task.due_date < start_tomorrow_utc
    ).order_by(Task.due_date.asc()).all()

    return tasks


def get_upcoming_tasks(db : Session, user_id: int ):

    # Gets the current UTC datetime
    now = utc_now()

    # Find incomplete tasks that belong to the user
    # and have a future due_date.
    tasks = db.query(Task).filter(
        Task.user_id ==  user_id,
        Task.is_complete  == False,
        Task.due_date.isnot(None),
        Task.due_date > now ,
        

    ).order_by(Task.due_date.asc()).all() # orders by due_date in ascending form

    return tasks


def get_overdue_tasks(db: Session , user_id: int):

    now = utc_now()

    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date < now,
    ).order_by(Task.due_date.asc()).all()

    return tasks

def get_task_summary(db : Session, user_id : int , user_timezone : str):
    try:
        user_tz = ZoneInfo(user_timezone)
    except Exception:
        user_tz = timezone.utc

    now_user_time = utc_now().astimezone(user_tz)

    start_today_user_time = datetime.combine(
        now_user_time.date(),
        time.min,
        tzinfo=user_tz
    )
   
    now = utc_now() 
    start_tomorrow_user_time = start_today_user_time + timedelta(days=1)

    start_today_utc = start_today_user_time.astimezone(timezone.utc)
    start_tomorrow_utc = start_tomorrow_user_time.astimezone(timezone.utc)

    due_today_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date >= start_today_utc,
        Task.due_date < start_tomorrow_utc
    ).count()


    upcoming_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date > now


    ).count()

    completed_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == True
    ).count()

    overdue_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.is_complete == False,
        Task.due_date.isnot(None),
        Task.due_date < now
    ).count()

    high_impact_count = db.query(Task).filter(
        Task.user_id == user_id,
        Task.impact_level == "high"
    ).count()

    return {
        "due_today": due_today_count,
        "upcoming": upcoming_count,
        "completed": completed_count,
        "overdue": overdue_count,
        "high_impact": high_impact_count
    }



