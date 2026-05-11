from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    login_id: str
    password: str