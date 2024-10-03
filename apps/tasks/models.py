from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, Enum
from sqlalchemy.orm import relationship

from apps.tasks.schemas import StatusType
from config.db import Base

class ModelCategory(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

class ModelTask(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(Text)
    status = Column(Enum(StatusType))
    category = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    image = Column(String)
    
    fk_category = relationship("ModelCategory", lazy="joined")

class ModelUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True, default="")
    website = Column(String(50), unique=True, default="")