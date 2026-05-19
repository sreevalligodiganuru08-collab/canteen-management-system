from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationModel(BaseModel):
    user_email: str

    title: str

    message: str

    notification_type: Optional[str] = "general"

    is_read: Optional[bool] = False

    created_at: Optional[datetime] = datetime.utcnow()