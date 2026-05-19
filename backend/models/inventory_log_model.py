from pydantic import BaseModel
from datetime import datetime


class InventoryLogModel(BaseModel):
    item_id: str

    item_name: str

    previous_stock: int

    updated_stock: int

    updated_by: str

    action: str

    created_at: datetime = datetime.utcnow()