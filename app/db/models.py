from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String

from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey , String , UniqueConstraint

class User(Base):

    __tablename__ ="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50),nullable=False,unique=True) 
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")
    categories: Mapped[List["Category"]] = relationship(back_populates="user")
class Task(Base):
    __tablename__="tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    due_date : Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at :  Mapped[Optional[datetime]]  = mapped_column(default=None, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="tasks")

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )

    category: Mapped[Optional["Category"]] = relationship(back_populates="tasks")


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_category_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="categories")

    tasks: Mapped[List["Task"]] = relationship(back_populates="category")