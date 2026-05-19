from fastapi import APIRouter, Depends
from datetime import datetime, timedelta

from database import (
    users_collection,
    items_collection,
    orders_collection,
    payments_collection,
    notifications_collection,
    offers_collection,
    combos_collection
)

from middleware.auth_middleware import (
    admin_required
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =====================================
# MAIN DASHBOARD STATS
# =====================================
@router.get("/stats")
def dashboard_stats(
    admin: dict = Depends(admin_required)
):

    total_users = users_collection.count_documents({
        "role": "user"
    })

    total_delivery_partners = users_collection.count_documents({
        "role": "delivery"
    })

    total_items = items_collection.count_documents({})

    total_combos = combos_collection.count_documents({})

    active_offers = offers_collection.count_documents({})

    total_orders = orders_collection.count_documents({})

    delivered_orders = orders_collection.count_documents({
        "status": "Delivered"
    })

    pending_orders = orders_collection.count_documents({
        "status": "Pending"
    })

    cancelled_orders = orders_collection.count_documents({
        "status": "Cancelled"
    })

    total_revenue = 0

    verified_revenue = 0

    orders = list(
        orders_collection.find()
    )

    for order in orders:

        total_revenue += order.get(
            "total_amount",
            0
        )

        if order.get(
            "payment_status"
        ) == "Verified":

            verified_revenue += order.get(
                "total_amount",
                0
            )

    low_stock_items = []

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

            low_stock_items.append({

                "item_name": item["name"],

                "remaining_stock": item[
                    "quantity"
                ]
            })

    unread_notifications = notifications_collection.count_documents({
        "is_read": False
    })

    pending_payments = payments_collection.count_documents({
        "payment_status": "Verification Pending"
    })

    return {

        "users": total_users,

        "delivery_partners": total_delivery_partners,

        "menu_items": total_items,

        "active_combos": total_combos,

        "active_offers": active_offers,

        "orders": {

            "total_orders": total_orders,

            "delivered_orders": delivered_orders,

            "pending_orders": pending_orders,

            "cancelled_orders": cancelled_orders
        },

        "revenue": {

            "total_revenue": total_revenue,

            "verified_revenue": verified_revenue
        },

        "inventory": {

            "low_stock_items": low_stock_items
        },

        "payments": {

            "pending_verifications": pending_payments
        },

        "notifications": {

            "unread_notifications": unread_notifications
        }
    }


# =====================================
# RECENT ORDERS
# =====================================
@router.get("/recent-orders")
def recent_orders(
    admin: dict = Depends(admin_required)
):

    orders = list(
        orders_collection.find()
        .sort("created_at", -1)
        .limit(10)
    )

    for order in orders:

        order["_id"] = str(order["_id"])

    return orders


# =====================================
# RECENT PAYMENTS
# =====================================
@router.get("/recent-payments")
def recent_payments(
    admin: dict = Depends(admin_required)
):

    payments = list(
        payments_collection.find()
        .sort("created_at", -1)
        .limit(10)
    )

    for payment in payments:

        payment["_id"] = str(payment["_id"])

    return payments


# =====================================
# ACTIVE OFFERS
# =====================================
@router.get("/offers")
def dashboard_offers(
    admin: dict = Depends(admin_required)
):

    offers = list(
        offers_collection.find()
    )

    for offer in offers:

        offer["_id"] = str(offer["_id"])

    return offers


# =====================================
# ACTIVE COMBOS
# =====================================
@router.get("/combos")
def dashboard_combos(
    admin: dict = Depends(admin_required)
):

    combos = list(
        combos_collection.find()
    )

    for combo in combos:

        combo["_id"] = str(combo["_id"])

    return combos


# =====================================
# LOW STOCK ALERTS
# =====================================
@router.get("/low-stock")
def low_stock_items(
    admin: dict = Depends(admin_required)
):

    items = list(
        items_collection.find()
    )

    low_stock = []

    for item in items:

        threshold = item.get(
            "low_stock_threshold",
            5
        )

        if item.get(
            "quantity",
            0
        ) <= threshold:

            item["_id"] = str(item["_id"])

            low_stock.append(item)

    return low_stock