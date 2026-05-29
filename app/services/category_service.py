from sqlalchemy.orm import Session
from app.db.models import Category
from fastapi.exceptions import HTTPException

from app.schemas.categories import CategoryCreate, CategoryUpdate


def get_categories_for_user(db: Session, user_id):
    categories = db.query(Category).filter(Category.user_id == user_id).all()
    return categories

def get_category_for_user(db: Session, user_id, category_id):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id
    ).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def create_category(db: Session, user_id, category: CategoryCreate):
    existing_category = db.query(Category).filter(
        Category.user_id == user_id,
        Category.name == category.name,

    ).first()

    if existing_category:
        raise HTTPException(status_code=409, detail="Category already exists")
    
    
    new_category = Category(
        name=category.name,
        user_id=user_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category(db: Session, user_id, category_id, category: CategoryUpdate):
    found_category = get_category_for_user(
        db=db,
        user_id=user_id,
        category_id=category_id,
    )
    if category.name is not None:
        existing_category = db.query(Category).filter(
            Category.user_id == user_id,
            Category.name == category.name,
            Category.id != category_id
        ).first()

        if existing_category:
            raise HTTPException(status_code=409, detail="Category already exists")
        
        found_category.name = category.name

    db.commit()
    db.refresh(found_category)

    return found_category

def delete_category(db: Session, user_id, category_id):
    found_category = get_category_for_user(
        db=db,
        user_id=user_id,
        category_id=category_id,
    )
    
    db.delete(found_category)
    db.commit()


    