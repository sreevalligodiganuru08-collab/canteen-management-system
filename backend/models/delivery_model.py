from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeliveryPartnerModel(BaseModel):
    name: str
    email: str
    phone: str
    city: str
    area: str

    vehicle_type: Optional[str] = "Bike"

    is_available: Optional[bool] = True

    current_order_id: Optional[str] = None

    joined_at: Optional[datetime] = datetime.utcnow()