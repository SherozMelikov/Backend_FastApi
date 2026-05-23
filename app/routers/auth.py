from fastapi import APIRouter, Depends 
from  typing import Annotated
from app.services.auth_service import login_user
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.schemas.token import TokenResponse

router = APIRouter(tags=["auth"])



@router.post("/login",response_model=TokenResponse)
async def  login(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    db : Annotated[Session, Depends(get_db)],

):
  return login_user(
    db=db,
    username=form_data.username,
    password=form_data.password
  )