from typing import Annotated

from fastapi import Depends, HTTPException , status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions  import InvalidTokenError
from sqlalchemy.orm import Session 
from app.core.security import decode_access_token
from app.db.database import get_db
from app.schemas.token import TokenData
from app.services.user_services import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: Annotated[str , Depends(oauth2_scheme)], db : Session = Depends(get_db)):
   credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers= {"WWW-Authenticate": "Bearer"},

   )
   try:
      payload = decode_access_token(token)
      print("PAYLOAD:", payload)

      username = payload.get("sub")
      print("USERNAME:", username)     
      
      
      if username is None:
         raise credentials_exception
      
      token_data = TokenData(username=username)
   

   except InvalidTokenError:
      raise credentials_exception
   user = get_user_by_username(db,username=token_data.username)

   if user is None:
      raise credentials_exception
   return user
      

