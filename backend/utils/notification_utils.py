from datetime import datetime

from database import (
    notifications_collection
)


# =====================================
# SEND NOTIFICATION
# =====================================
def send_notification(
    user_email,
    title,
    message,
    notification_type="general"
):

    notifications_collection.insert_one({

        "user_email": user_email,

        "title": title,

        "message": message,

        "notification_type": notification_type,

        "is_read": False,

        "created_at": datetime.utcnow()
    })


# =====================================
# MARK AS READ
# =====================================
def mark_notification_read(
    notification_id
):

    notifications_collection.update_one(
        {"_id": notification_id},
        {
            "$set": {
                "is_read": True
            }
        }
    )