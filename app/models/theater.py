from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base
from app.models.user import User

# Theater model
class Theater(Base):
    __tablename__ = "theaters"
    

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)  # Store UUID as string
    name = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=False)
    contact_info = Column(String, nullable=False)
    admins = relationship("User", secondary="theater_admins", back_populates="theaters")
    images = relationship("Image", back_populates="theater")
    screens = relationship("Screen", back_populates="theater")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Image model
class Image(Base):
    __tablename__ = "images"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Store UUID as string
    image_url = Column(String, nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    theater = relationship("Theater", back_populates="images")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Screen(Base):
    __tablename__ = "screens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    theater = relationship("Theater", back_populates="screens")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Junction table for many-to-many relationship
class TheaterAdmin(Base):
    __tablename__ = "theater_admins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    user = relationship("User", back_populates="theaters")
    theater = relationship("Theater", back_populates="admins")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

