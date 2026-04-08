from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int]
    is_active: bool
    created_at: datetime