

from fastapi import HTTPException , status 

from app.schemas.token import TokenResponse
from app.services.user_services import get_user_by_username
from app.core.security import verify_password , create_access_token


def authenticate_user(db, username: str , password: str):
   user =  get_user_by_username(db,username)

   if not user:
      return False
   if not verify_password(password, user.hashed_password):
      return False
   return user


def login_user(db,username, password) -> TokenResponse:
    user = authenticate_user(db ,username,password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},

        )

    access_token = create_access_token(
       data={"sub": user.username}
    )
    return TokenResponse(access_token=access_token, token_type="bearer")


