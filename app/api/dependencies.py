
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.crud import crud_user
from app.db.session import sessionLocal
from sqlalchemy.orm import Session
from jose import jwt

from app.models.user import User
from app.schemas.token import TokenData
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session= Depends(get_db), token:str = Depends(oauth2_scheme)):
    CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise CredentialsException
    user = crud_user.crud_user.get_by_email(db, email=token_data.email)
    if user is None:
        raise CredentialsException
    return user


def get_current_admin_user(current_user: User = Depends(get_current_user), ):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user