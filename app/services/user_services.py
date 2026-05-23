from fastapi import HTTPException , status
from sqlalchemy.orm import Session 

from app.db.models import User
from app.schemas.users import UserCreate, UserResponse
from app.core.security import create_access_token, hash_password, verify_password


## It is not sugested to use  HTTPException inside the helpers like 
# def get)user_by_username  instead  use it inside the 

def read_users(db: Session):
    users = db.query(User).all()
    return users


def create_users(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_id(db: Session, user_id: int):
    user_by_id = db.query(User).filter(User.id == user_id).first()
    return user_by_id

def get_user_by_email(db : Session , user_email : str):
    user_by_email = db.query(User).filter(User.email== user_email).first()
    return user_by_email


def get_user_by_username(db: Session, username: str):
  
    user_by_username = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    return user_by_username



def register_user(db: Session , user : UserCreate):

    """
    Register a new user.

    Parameters:
    - db: database session used to query and save users
    - user: validated signup data from UserCreate schema
      contains username, email, and plain password

    Flow:
    1. Check if username already exists
    2. Check if email already exists
    3. If both are available, create the user
    4. Return the newly created user
    """

    # Check whether the required username already exists  in the database.
    # user,username comes from  the UserCreate request schema.
    existing_username = get_user_by_username(db, user.username)

    # if a user object is returned , the username is already taken.
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"

        )
    
    # Check whether the requested  email  already exists  in the database.
    # user.email comes from the UserCreate request  schema.
    existing_email = get_user_by_email(db, user.email)

    # If a user  object  is returned  , the email is already registered 
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
            
        )
    # If username  and  email are available , create the user.
    # create_users handles hashing the password and saving  the user.
    new_user = create_users(db, user)

    # Return the newly created  database user.
    return new_user 

