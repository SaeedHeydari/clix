from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    english_title = Column(String(255))
    description = Column(Text)
    image = Column(String(500))
    icon = Column(String(500))
    category_parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    brand = Column(String(255))
    order = Column(Integer, default=0)
    visible = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    filterable_by_brand = Column(Boolean, default=False)
    background_color = Column(String(20))
    absolute_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Self-referential relationship for parent-child categories
    #parent = relationship("Category", remote_side=[id], backref="children")

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    name1 = Column(String(255), nullable=False)  # Persian name
    name2 = Column(String(255), nullable=False)  # English name
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to Category
    category = relationship("Category", backref="brands")
