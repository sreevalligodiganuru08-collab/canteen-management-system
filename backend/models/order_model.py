from pydantic import BaseModel
from typing import List


class OrderItem(BaseModel):
    item_id: str
    quantity: int


class OrderCreate(BaseModel):
    user_email: str
    items: List[OrderItem]