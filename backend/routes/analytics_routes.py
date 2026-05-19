from fastapi import APIRouter, Depends

from database import (
    orders_collection,
    items_collection,
    users_collection
)

from middleware.auth_middleware import (
    admin_required
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# =====================================
# SALES ANALYTICS
# =====================================
@router.get("/sales")
def sales_analytics(
    admin: dict = Depends(admin_required)
):

    orders = list(
        orders_collection.find()
    )

    total_sales = 0

    total_orders = len(orders)

    delivered_orders = 0

    cancelled_orders = 0

    pending_orders = 0

    for order in orders:

        total_sales += order.get(
            "total_amount",
            0
        )

        status = order.get(
            "status",
            "Pending"
        )

        if status == "Delivered":

            delivered_orders += 1

        elif status == "Cancelled":

            cancelled_orders += 1

        else:

            pending_orders += 1

    return {

        "total_sales": total_sales,

        "total_orders": total_orders,

        "delivered_orders": delivered_orders,

        "cancelled_orders": cancelled_orders,

        "pending_orders": pending_orders
    }


# =====================================
# INVENTORY ANALYTICS
# =====================================
@router.get("/inventory")
def inventory_analytics(
    admin: dict = Depends(admin_required)
):

    items = list(
        items_collection.find()
    )

    total_items = len(items)

    low_stock_items = []

    out_of_stock_items = []

    for item in items:

        quantity = item.get(
            "quantity",
            0
        )

        if quantity == 0:

            out_of_stock_items.append({

                "name": item["name"],

                "quantity": quantity
            })

        elif quantity <= 5:

            low_stock_items.append({

                "name": item["name"],

                "quantity": quantity
            })

    return {

        "total_items": total_items,

        "low_stock_items": low_stock_items,

        "out_of_stock_items": out_of_stock_items
    }


# =====================================
# USERS ANALYTICS
# =====================================
@router.get("/users")
def users_analytics(
    admin: dict = Depends(admin_required)
):

    total_users = users_collection.count_documents({
        "role": "user"
    })

    total_admins = users_collection.count_documents({
        "role": "admin"
    })

    total_delivery_partners = users_collection.count_documents({
        "role": "delivery"
    })

    return {

        "total_users": total_users,

        "total_admins": total_admins,

        "total_delivery_partners": total_delivery_partners
    }