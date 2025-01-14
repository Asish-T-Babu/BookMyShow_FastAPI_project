from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: str
    username: str
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserInDB(User):
    password: str


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., max_length=100)
    email: EmailStr