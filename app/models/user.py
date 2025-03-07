from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base
from app.enums.model_enums import *
from app.flags import USER, ACTIVE, INACTIVE, DELETED
# from app.models.theaters import TheaterAdmin

class User(Base):
    __tablename__ = 'users'


    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    dob = Column(DateTime)
    gender = Column(Integer)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    role = Column(Integer, default=USER)
    theaters = relationship("Theater", secondary="theater_admins", back_populates="admins")
    theater_admins = relationship("TheaterAdmin", back_populates="user")
    status = Column(Integer, default=ACTIVE, nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
