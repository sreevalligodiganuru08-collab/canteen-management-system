from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemCreate(BaseModel):
    name: str
    price: float
    quantity: int
    category: str
    image_path: str
    description: str

    available: Optional[bool] = True

    sold_count: Optional[int] = 0

    low_stock_threshold: Optional[int] = 5

    offer_percentage: Optional[float] = 0

    created_at: Optional[datetime] = datetime.utcnow()


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    image_path: Optional[str] = None
    description: Optional[str] = None

    available: Optional[bool] = None

    sold_count: Optional[int] = None

    low_stock_threshold: Optional[int] = None

    offer_percentage: Optional[float] = None