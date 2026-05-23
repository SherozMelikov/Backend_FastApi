from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class User(Base):

    __tablename__ ="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50),nullable=False,unique=True) 
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
 

class Task(Base):
    __tablename__="tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")
