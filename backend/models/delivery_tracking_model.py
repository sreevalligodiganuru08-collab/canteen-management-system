from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeliveryTrackingModel(BaseModel):
    order_id: str

    delivery_partner_email: str

    current_status: str

    current_location: Optional[str] = ""

    destination_location: Optional[str] = ""

    reached_destination: Optional[bool] = False

    delivered_successfully: Optional[bool] = False

    updated_at: Optional[datetime] = datetime.utcnow()