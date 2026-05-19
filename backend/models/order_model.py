from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItem(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int
    image_path: str
    subtotal: float


class OrderModel(BaseModel):
    user_email: str

    items: List[OrderItem]

    total_amount: float

    status: Optional[str] = "Pending"

    payment_method: Optional[str] = "COD"

    payment_status: Optional[str] = "Pending"

    delivery_partner_email: Optional[str] = None

    delivery_status: Optional[str] = "Waiting"

    user_location: Optional[str] = ""

    assigned_city: Optional[str] = ""

    assigned_area: Optional[str] = ""

    delivered_at: Optional[datetime] = None

    created_at: Optional[datetime] = datetime.utcnow()