from fastapi import APIRouter, Depends

from database import (
    users_collection,
    orders_collection
)

from middleware.auth_middleware import (
    admin_required
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =====================================
# DASHBOARD STATS
# =====================================
@router.get("/stats")
def dashboard_stats(
    admin: dict = Depends(admin_required)
):

    total_users = users_collection.count_documents({
        "role": "user"
    })

    total_orders = orders_collection.count_documents({})

    pending_orders = orders_collection.count_documents({
        "order_status": "Pending"
    })

    preparing_orders = orders_collection.count_documents({
        "order_status": "Preparing"
    })

    delivered_orders = orders_collection.count_documents({
        "order_status": "Delivered"
    })

    all_orders = list(
        orders_collection.find()
    )

    total_revenue = 0

    for order in all_orders:

        payment_status = order.get(
            "payment_status",
            "Pending"
        )

        total_amount = order.get(
            "total_amount",
            0
        )

        if payment_status == "Paid":

            total_revenue += total_amount

    return {

        "total_users": total_users,

        "total_orders": total_orders,

        "pending_orders": pending_orders,

        "preparing_orders": preparing_orders,

        "delivered_orders": delivered_orders,

        "total_revenue": total_revenue
    }