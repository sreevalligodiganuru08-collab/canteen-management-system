from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OfferModel(BaseModel):
    item_id: str

    offer_title: str

    discount_percentage: float

    description: Optional[str] = ""

    active: Optional[bool] = True

    created_at: Optional[datetime] = datetime.utcnow()