




from sqlalchemy import Column, Integer, String, DateTime
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1, nullable=False)
    is_admin = Column(Integer, default=0, nullable=False)
    otp = Column(String(6), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)