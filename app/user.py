from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# This is what the user sends when they SIGN UP
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

# This is what we send BACK to the user (notice we don't send the password!)
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True