# валидация

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel): # создание, данные идут с cli
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserUpdate(BaseModel): # обновление
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None

class User(BaseModel): # main model
    id: int
    name: str
    email: EmailStr
    age: Optional[int]
    is_active: bool
    created_at: datetime