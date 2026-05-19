from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CartModel(BaseModel):
    user_email: str

    item_id: str

    name: str

    price: float

    quantity: int

    image_path: str

    subtotal: Optional[float] = 0

    available: Optional[bool] = True

    added_at: Optional[datetime] = datetime.utcnow()