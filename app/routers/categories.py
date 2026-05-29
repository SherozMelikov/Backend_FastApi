from typing import Annotated

from fastapi import APIRouter, Depends , status

from app.db.database import get_db
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from sqlalchemy.orm import Session

from app.services import category_service 

router = APIRouter(prefix="/categories", tags=["categories"])



@router.get("/", response_model=list[CategoryResponse])
def read_categories(
    current_user : Annotated [User, Depends(get_current_user)],
    db: Session = Depends(get_db),

):
    return category_service.get_categories_for_user(
        db=db,
        user_id=current_user.id,
    )
    

@router.get("/{category_id}", response_model=CategoryResponse)
def read_category_by_id(
    category_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return category_service.get_category_for_user(
        db=db,
        user_id=current_user.id,
        category_id=category_id,
    )


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category : CategoryCreate,
    current_user : Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    
    return category_service.create_category(
        db=db,
        user_id=current_user.id,
        category=category
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    category_service.delete_category(
        db=db,
        user_id=current_user.id,
        category_id=category_id,
    )

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return category_service.update_category(
        db=db,
        user_id=current_user.id,
        category_id=category_id,
        category=category,
    )
