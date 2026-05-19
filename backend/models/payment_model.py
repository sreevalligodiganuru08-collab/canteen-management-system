from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentModel(BaseModel):
    order_id: str

    user_email: str

    payment_method: str

    payment_status: Optional[str] = "Pending"

    collected_amount: Optional[float] = 0

    payment_proof_image: Optional[str] = ""

    collected_by_delivery: Optional[bool] = False

    verified_by_admin: Optional[bool] = False

    created_at: Optional[datetime] = datetime.utcnow()