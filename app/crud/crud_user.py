from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User 
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str):
        return db.query(self.model).filter(self.model.email == email).first()

    def create(
        self,
        db: Session,
        *,
        obj_in: UserCreate,
        otp: str,
        otp_expiry: datetime
    ):
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            hashed_password=obj_in.password,
            is_active=False,
            is_admin=False,
            otp=otp,
            otp_expiry=otp_expiry,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def verify_otp(self, db: Session, *, email: str,otp:str):
        user = self.get_by_email(db, email=email)
        if user and user.otp ==otp and user.otp_expiry > datetime.utcnow():
            user.is_active = True
            db.commit()
            db.refresh(user)
            return user
    
    def authenticate(self, db: Session, *,email:str, password:str):
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not user.is_active:
            return None
        if not user.hashed_password == password:
            return None
        return user
    
crud_user = CRUDUser(User)
