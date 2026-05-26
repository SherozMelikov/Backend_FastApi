from sqlalchemy.orm import Session
from app.db.models import Category
from fastapi.exceptions import HTTPException

from app.schemas.tasks import CategoryCreate, CategoryUpdate

def get_categories_for_user(db: Session, user_id: int):
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    return categories

def get_category_for_user(db: Session, user_id: int, category_id: int):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def create_category(db: Session, user_id: int, category: CategoryCreate):
    new_category = Category(
        name=category.name,
        user_id=user_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category(db: Session, user_id: int, category_id: int, category: CategoryUpdate):
    found_category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

    if found_category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    found_category.name = category.name
    

    db.commit()
    db.refresh(found_category)

    return found_category

def delete_category(db: Session, user_id: int, category_id: int):
    found_category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()

    if not found_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(found_category)
    db.commit()

    return {"message": "Category is successfully deleted!"}

    