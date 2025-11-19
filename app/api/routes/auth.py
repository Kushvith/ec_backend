


from datetime import datetime, timedelta
import random
from fastapi import APIRouter, BackgroundTasks, HTTPException,status
from fastapi.params import Depends

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import create_access_token
from app.crud.crud_user import crud_user
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.user import UserCreate

from app.services.email_services import send_otp_email

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
    
    background_tasks.add_task(send_otp_email, user.email, otp)
    return user
@router.post("/verify-otp")
def verify_otp(*, db: Session = Depends(get_db),email: str,otp: str):
    user =  crud_user.verify_otp(db, email=email,otp=otp)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP",
        )
    return {"message": "OTP verified successfully"}

@router.post("/login")
def login(*, db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.authenticate(db,email=form_data.username, password=form_data.password)
    if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect username or password",
           headers={"WWW-Authenticate": "Bearer"},
       )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
    
    