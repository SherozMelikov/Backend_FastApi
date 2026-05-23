#Import SQLAlchemy Session  type  for a database  operations
from typing import Annotated

from sqlalchemy.orm import Session

#Import database dependency that provides  a DB Session 
from app.db.database import get_db

#Import  HTTPException to handle  error  with logs 

from fastapi import HTTPException

#Import SQLAlchemy  model / table
from app.db.models import Task, User

# Import  FastAPI router and dependency Helper 
from fastapi  import APIRouter  , Depends

# Import Pydantic schemas  for request  validation  response formatting
from  app.dependencies.auth  import get_current_user 
from  app.schemas.tasks  import TaskCreate , TaskResponse , TaskUpdate
from app.services import task_services



router = APIRouter()


#  GET /tasks/ 
# Retrives  all tasks from the db
@router.get("/tasks/" , tags=["tasks"] , response_model=list[TaskResponse])
def read_tasks (
    current_user: Annotated[User, Depends(get_current_user)],
    db : Session = Depends(get_db),
   
): 
    user_id = current_user.id
    tasks = task_services.get_tasks_for_user(
        db=db,
        user_id=user_id
    )
    return tasks
       


# Get /task/{task_id}
# Teturns task by it is id 
@router.get("/tasks/{task_id}", tags=["tasks"],response_model=TaskResponse)
def read_task_by_id(
    task_id : int, 
    current_user : Annotated[User, Depends(get_current_user)],
    db : Session = Depends(get_db),
    
):
    user_id = current_user.id
    task = task_services.get_task_for_user(
        db=db,
        user_id=user_id,
        task_id=task_id
        
    )

    return task

# PUT /tasks/{task_id}
#  Finds  an existing  task by ID , update its fields, saves changes , and returns the updated task.
@router.put("/tasks/{task_id}", tags=["tasks"], response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    user : Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    user_id = user.id
    update_task_for_user  = task_services.put_task(
        db=db,
        user_id=user_id,
        task=task,
        task_id=task_id

    )
    return update_task_for_user

# Delete /tasks {task_id}
# Finds a task by ID , deletes  it if  it exists  , and returns 200 No content!

@router.delete("/tasks/{task_id}",tags=["tasks"], status_code=200)
def delete_task_by_id(
    task_id : int , 
    user : Annotated [ User , Depends (get_current_user)],
    db : Session = Depends(get_db)

):
    
    return task_services.delete_task(
        db=db,
        user_id=user.id,
        task_id=task_id
        
    )



# Post /tasks/ 
# Create a task  and saves to db !
@router.post("/tasks/",response_model=TaskResponse,tags=["tasks"])
def create_tasks(
    task : TaskCreate,
    user : Annotated[User, Depends(get_current_user)],
    db : Session = Depends(get_db)
):
    
    
    return  task_services.post_task(
       db=db,
       user_id=user.id,
       task=task,
       

       
   )