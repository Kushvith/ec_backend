


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),unique=True,index=True, nullable=False)
    image_url = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
