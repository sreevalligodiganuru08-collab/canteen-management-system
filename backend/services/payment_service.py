from database import (
    payments_collection
)


# =====================================
# UPDATE PAYMENT STATUS
# =====================================
def update_payment_status(
    order_id: str,
    status: str
):

    payments_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {
                "payment_status": status
            }
        }
    )