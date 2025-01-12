from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.utils import hash_password
from app.models.user_models import User
from app.schemas.user_models_schemas import UserCreate

router = APIRouter()

@router.post("/create")
async def create_user(user: Annotated[UserCreate, Form()], db: Session = Depends(get_db)):
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new user object
    new_user = User(
        username=user.username,
        password=hashed_password,
        first_name=user.first_name,
    )

    # Add and commit the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username, "first_name": new_user.first_name}
