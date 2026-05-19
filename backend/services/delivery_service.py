from database import (
    orders_collection
)

from bson import ObjectId


# =====================================
# ASSIGN DELIVERY PARTNER
# =====================================
def assign_delivery_partner(
    order_id: str,
    delivery_email: str
):

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {

                "delivery_partner": delivery_email,

                "delivery_status": "Assigned"
            }
        }
    )