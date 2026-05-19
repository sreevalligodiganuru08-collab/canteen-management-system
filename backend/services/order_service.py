from datetime import datetime

from database import (
    orders_collection,
    cart_collection
)

from services.cart_service import (
    calculate_cart_total
)


# =====================================
# CREATE ORDER
# =====================================
def create_order_service(
    user_email: str,
    items: list
):

    total_amount = calculate_cart_total(
        user_email
    )

    order_data = {

        "user_email": user_email,

        "items": items,

        "total_amount": total_amount,

        "status": "Pending",

        "payment_status": "Pending",

        "delivery_status": "Waiting",

        "created_at": datetime.utcnow()
    }

    result = orders_collection.insert_one(
        order_data
    )

    cart_collection.delete_many({
        "user_email": user_email
    })

    return str(result.inserted_id)