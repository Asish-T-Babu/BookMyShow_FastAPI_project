from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.schemas.user import UserSchema


class LocationCreate(BaseModel):
    city: str = Field(..., max_length=100, description="The city of the location")
    state: str = Field(..., max_length=100, description="The state of the location")
    country: str = Field(..., max_length=100, description="The country of the location")
    pincode: str = Field(..., max_length=20, description="The postal or zip code of the location")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "New York",
                "state": "NY",
                "country": "USA",
                "pincode": "10001"
            }
        }


class LocationResponse(LocationCreate):
    id: str
    created_by: Optional[UserSchema]

    class Config:
        from_attributes = True 


class TheaterCreate(BaseModel):
    name: str
    location: str
    contact_info: str

class ImageUpload(BaseModel):
    image_url: str

class ScreenCreate(BaseModel):
    name: str
    capacity: int

class AdminConnect(BaseModel):
    user_id: UUID

# Response Schemas
class TheaterResponse(BaseModel):
    id: UUID
    name: str
    location: str
    contact_info: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
