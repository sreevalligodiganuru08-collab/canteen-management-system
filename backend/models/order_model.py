from pydantic import BaseModel
from typing import List
from datetime import datetime


# ==============================
# ORDER ITEM
# ==============================
class OrderItem(BaseModel):

    item_id: str
    name: str
    price: float
    quantity: int
    image_path: str
    subtotal: float


# ==============================
# ORDER MODEL
# ==============================
class OrderModel(BaseModel):

    user_email: str

    items: List[OrderItem]

    total_amount: float

    payment_method: str

    payment_status: str = "Pending"

    order_status: str = "Pending"

    pickup_token: str

    estimated_time: str

    created_at: datetime = datetime.utcnow()

    delivered_at: datetime = None