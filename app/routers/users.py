#Import SQLAlchemy  Session   type for a database  operations 
from typing import Annotated

from sqlalchemy.orm import Session
#Import database dependency that provides  a DB Session
from app.db.database import get_db#
#Import SQLAlchemy  User  model/ table
from app.db.models import User
#Import FastAPI router and dendency helper
from fastapi import APIRouter, Depends
#Import Pydantic schemas for request validation and responses formatting
from app.dependencies.auth  import get_current_user
from app.schemas.token import TokenResponse
from app.schemas.users  import UserCreate, UserLogin, UserResponse

router = APIRouter()


from app.services import auth_service, user_services




@router.get("/users/current", tags=["users"], response_model=UserResponse)
async  def get_users_current(current_user : Annotated[User, Depends(get_current_user)]):
    return current_user


# GET /users/
# Retrives all users from the database
# response_model = list[UserResponse] means the API returns a list of users
# @router.get("/users/",response_model=list[UserResponse],tags=["users"])
# def  get_users(db : Session =  Depends(get_db)) :
#     return user_services.read_users(db=db)

# POST /users/
# Create a new user in the database
# UserCreate   validates  the incomming request  body
# UserResponse controls what data is returned  to the client 
@router.post("/users/",response_model=UserResponse,tags=["users"])
def post_users(user: UserCreate, db:  Session = Depends(get_db)):
    return user_services.register_user(db=db,user=user)




# GET /users/{user_id}
# Retrives one user from the database by ID 
# user_id comes from the URL path
# @router.get("/users/{user_id}",tags= ["users"], response_model=UserResponse) 
# def get_user_by_id(
#     user_id: int , # Path parameter.  The {user_id} from  the URL. FastAPI converts it to int 
#     db : Session =  Depends(get_db)  # Database session. Depends(get_db) gives this function access to the DB
      
# ):
#     return user_services.get_user_by_id(user_id=user_id,db=db)


# Post /user
# Create 
