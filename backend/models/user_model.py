from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ==============================
# USER REGISTER MODEL
# ==============================
class UserRegister(BaseModel):

    name: str

    email: EmailStr

    password: str

    phone: str

    role: Optional[str] = "customer"

    city: Optional[str] = ""

    area: Optional[str] = ""

    address: Optional[str] = ""

    profile_image: Optional[str] = ""

    is_active: Optional[bool] = True

    created_at: Optional[datetime] = datetime.utcnow()


# ==============================
# USER LOGIN MODEL
# ==============================
class UserLogin(BaseModel):

    email: EmailStr

    password: str


# ==============================
# USER RESPONSE MODEL
# ==============================
class UserResponse(BaseModel):

    id: str

    name: str

    email: EmailStr

    phone: str

    role: str

    city: Optional[str]

    area: Optional[str]

    address: Optional[str]

    profile_image: Optional[str]

    is_active: bool