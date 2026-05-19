from datetime import datetime

from database import (
    notifications_collection
)


# =====================================
# CREATE NOTIFICATION
# =====================================
def create_notification(
    user_email: str,
    title: str,
    message: str,
    notification_type: str
):

    notifications_collection.insert_one({

        "user_email": user_email,

        "title": title,

        "message": message,

        "notification_type": notification_type,

        "is_read": False,

        "created_at": datetime.utcnow()
    })