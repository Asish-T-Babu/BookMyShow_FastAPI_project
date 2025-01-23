from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from typing import Annotated, List
from datetime import timedelta

from app.database import get_db
from app.models.theater import Location
from app.models.user import User
from app.schemas.theater import LocationCreate, LocationResponse
from app.schemas.user import UserSchema
from app.core.settings import oauth2_scheme, ACCESS_TOKEN_EXPIRE_DAYS
from app.schemas.utils_shemas import Token
from app.flags import ACTIVE, INACTIVE, DELETED
from app.utils import token_validation

router = APIRouter()

@router.post("/create_location/" , response_model=LocationResponse)
def create_location(location_data: LocationCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = token_validation(token)
    print(user_id, 'user_id')
    existing_location = db.query(Location).filter(Location.country == location_data.country, Location.state == location_data.state, Location.city == location_data.city, Location.pincode == location_data.pincode).first()
    if existing_location:
        raise HTTPException(status_code=400, detail="Location already taken")

    location_data_dict = location_data.model_dump()
    location_data_dict['created_by'] = user_id
    new_location = Location(**location_data_dict)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    new_location = db.query(Location).filter(Location.id == new_location.id).first()
    print(new_location.__dict__)
    new_location.created_by = db.query(User).filter(User.id == new_location.created_by).first()
    return new_location


@router.get("/locations/", response_model=List[LocationResponse])
def get_all_locations(db: Session = Depends(get_db)):
    # Query all locations and include user data using joinedload
    locations = db.query(Location).all()
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found")
    
    location_responses = []
    for location in locations:
        created_by_user = (
            db.query(User).filter(User.id == location.created_by).first()
        )
        location_responses.append(
            LocationResponse(
                id=str(location.id),
                city=location.city,
                state=location.state,
                country=location.country,
                pincode=location.pincode,
                created_by=UserSchema.model_validate(created_by_user) if created_by_user else None
            )
        )
    return location_responses