

from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),unique=True,index=True, nullable=False)
    image_url = Column(String(255), nullable=True)

    