from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from app.database import get_db
from app.models.theater import Location
from app.schemas.theater import LocationCreate, LocationResponse
from app.core.settings import oauth2_scheme, ACCESS_TOKEN_EXPIRE_DAYS
from app.schemas.utils_shemas import Token
from app.flags import ACTIVE, INACTIVE, DELETED
from app.utils import token_validation

router = APIRouter()

@router.post("/create_location/" , response_model=LocationResponse)
def create_location(location_data: LocationCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = token_validation(token)
    existing_location = db.query(Location).filter(Location.country == location_data.country, Location.state == location_data.state, Location.city == location_data.city, Location.pincode == location_data.pincode).first()
    if existing_location:
        raise HTTPException(status_code=400, detail="Location already taken")

    location_data_dict = location_data.model_dump()
    location_data_dict['created_by'] = user_id
    new_location = Location(**location_data_dict)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location