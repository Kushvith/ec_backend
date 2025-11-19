


from datetime import datetime, timedelta
import random
from fastapi import APIRouter, BackgroundTasks, HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.user import UserCreate


router = APIRouter()

@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    background_tasks: BackgroundTasks
):
    """
    Create new user and send OTP.
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    otp = str(random.randint(100000, 999999))
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    user = crud_user.create(db=db, obj_in=user_in, otp=otp, otp_expiry=otp_expiry)
    return user