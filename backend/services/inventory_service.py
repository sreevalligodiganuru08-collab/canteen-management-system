from database import (
    items_collection,
    notifications_collection
)

from datetime import datetime


# =====================================
# CHECK LOW STOCK
# =====================================
def check_low_stock():

    items = list(
        items_collection.find()
    )

    for item in items:

        threshold = item.get(
            "low_stock_threshold",
            5
        )

        if item.get(
            "quantity",
            0
        ) <= threshold:

            existing = notifications_collection.find_one({

                "title": "Low Stock Alert",

                "message": f"{item['name']} is running low"
            })

            if not existing:

                notifications_collection.insert_one({

                    "user_email": "admin",

                    "title": "Low Stock Alert",

                    "message": f"{item['name']} is running low",

                    "notification_type": "inventory",

                    "is_read": False,

                    "created_at": datetime.utcnow()
                })