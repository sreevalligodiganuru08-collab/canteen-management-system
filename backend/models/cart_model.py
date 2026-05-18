from pydantic import BaseModel
from datetime import datetime


# ==============================
# ADD TO CART MODEL
# ==============================
class CartModel(BaseModel):
    user_email: str
    item_id: str
    name: str
    price: float
    quantity: int
    image_path: str
    added_at: datetime = datetime.utcnow()