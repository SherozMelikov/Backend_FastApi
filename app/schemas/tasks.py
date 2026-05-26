
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class TaskCreate(BaseModel):
    title : str = Field(
        min_length=1,
        max_length=100,
    )
    description : str | None = Field(default=None, max_length=500)
    is_complete : bool = False
    category_id : int | None = Field(default=None, gt=0)

class TaskUpdate(BaseModel):
    title : str = Field(
        min_length=1,
        max_length=100,
    ) 
    description : str | None = Field(default=None, max_length=500)
    is_complete : bool = False
    category_id: int | None = Field(default=None, gt=0)

class TaskResponse(BaseModel):
    id : int
    title: str
    description: str | None = None 
    is_complete: bool
    created_at : datetime 
    user_id : int 
    category_id: int | None = None
    model_config = ConfigDict(from_attributes=True)

