from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str
    phone_number: Optional[str] = None
    is_active: bool = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to receive via API on login for standard JSON login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Properties to return to client
class UserResponse(UserBase):
    id: UUID4
    created_at: datetime

    model_config = {"from_attributes": True}
