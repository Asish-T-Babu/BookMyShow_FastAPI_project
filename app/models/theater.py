from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.database import Base
from app.models.user import User
from app.flags import ACTIVE, INACTIVE, DELETED

# Theater model
class Location(Base):
    __tablename__ = "locations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)
    theaters = relationship("Theater", back_populates="location")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_by = Column(String(36), ForeignKey('users.id'))
    updated_by = Column(String(36), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Location(id={self.id}, city={self.city}, state={self.state}, country={self.country})>"

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)  # Store UUID as string
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    location_id = Column(String(36), ForeignKey("locations.id"), nullable=False)
    contact_info = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    admins = relationship("User", secondary="theater_admins", back_populates="theaters")
    theater_admins = relationship("TheaterAdmin", back_populates="theater")

    images = relationship("Image", back_populates="theater")
    screens = relationship("Screen", back_populates="theater")
    location = relationship("Location", back_populates="theaters")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Image model
class Image(Base):
    __tablename__ = "images"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Store UUID as string
    image_url = Column(String, nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    theater = relationship("Theater", back_populates="images")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Screen(Base):
    __tablename__ = "screens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    theater = relationship("Theater", back_populates="screens")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Junction table for many-to-many relationship
class TheaterAdmin(Base):
    __tablename__ = "theater_admins"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    theater_id = Column(String(36), ForeignKey("theaters.id"), nullable=False)
    user = relationship("User", back_populates="theater_admins")
    theater = relationship("Theater", back_populates="theater_admins")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

