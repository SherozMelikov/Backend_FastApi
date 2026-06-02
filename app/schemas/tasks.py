from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

TaskLevel = Literal["low","medium","high"]

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    is_complete: bool = False
    category_id: int | None = Field(default=None, gt=0)
    due_date: datetime | None = None
    priority : TaskLevel = "medium" 
    impact_level : TaskLevel = "medium" 

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    is_complete: bool | None = None
    category_id: int | None = Field(default=None, gt=0)
    due_date: datetime | None = None
    priority : TaskLevel | None = None
    impact_level : TaskLevel | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_complete: bool
    created_at: datetime
    due_date: datetime | None = None
    completed_at: datetime | None = None
    user_id: int
    category_id: int | None = None
    priority : TaskLevel 
    impact_level : TaskLevel

    model_config = ConfigDict(from_attributes=True)