

import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user, get_db
from app.crud import crud_category

from app.models.user import User
from app.schemas.category import Category

router = APIRouter()

UPLOAD_FOLDER = "static/categories"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/")
def create_category(
    *,
    db: Session = Depends(get_db),
    name: str = Form(...),
    image: str = Form(...),
    current_admin: User = Depends(get_current_admin_user),
):
    file_path = os.path.join(UPLOAD_FOLDER, image)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    img_url = f"/{file_path}"
    category_in = crud_category.category.create(db, name=name, image_url=img_url)
    return category_in

@router.get("/",response_model=None)
def get_categories(db:Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    return crud_category.category.get_multi(db)

@router.delete("/{category_id}")
def delete_category(category_id: int,db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin_user)):  
    
    category = crud_category.category.get(db, id=category_id)  
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.image_url:
        image_path = category.image_url[1:]
        if os.path.exists(image_path):
            os.remove(image_path)
    return crud_category.category.remove(db, id=category_id)