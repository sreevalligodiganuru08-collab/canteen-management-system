from pydantic import BaseModel
from typing import Optional


# ==============================
# CREATE ITEM MODEL
# ==============================
class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category: str
    image_path: str
    description: str


# ==============================
# UPDATE ITEM MODEL
# ==============================
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None
    available: Optional[bool] = None