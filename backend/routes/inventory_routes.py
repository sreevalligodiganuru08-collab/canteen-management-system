from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import (
    items_collection,
    inventory_logs_collection,
    notifications_collection
)

from middleware.auth_middleware import (
    admin_required
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


# =====================================
# UPDATE STOCK
# =====================================
@router.put("/update-stock/{item_id}")
def update_stock(
    item_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    new_stock = data.get("quantity")

    if new_stock is None:

        raise HTTPException(
            status_code=400,
            detail="Quantity is required"
        )

    previous_stock = item["quantity"]

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$set": {
                "quantity": new_stock
            }
        }
    )

    # INVENTORY LOG
    inventory_logs_collection.insert_one({

        "item_id": item_id,

        "item_name": item["name"],

        "previous_stock": previous_stock,

        "updated_stock": new_stock,

        "updated_by": admin["email"],

        "action": "Stock Updated",

        "created_at": datetime.utcnow()
    })

    return {
        "message": "Stock updated successfully"
    }


# =====================================
# LOW STOCK ITEMS
# =====================================
@router.get("/low-stock")
def low_stock_items(
    admin: dict = Depends(admin_required)
):

    items = list(items_collection.find())

    low_stock = []

    for item in items:

        threshold = item.get(
            "low_stock_threshold",
            5
        )

        if item["quantity"] <= threshold:

            item["_id"] = str(item["_id"])

            low_stock.append(item)

    return low_stock


# =====================================
# AUTO LOW STOCK ALERTS
# =====================================
@router.post("/check-alerts")
def check_low_stock_alerts(
    admin: dict = Depends(admin_required)
):

    items = list(items_collection.find())

    alerts = []

    for item in items:

        threshold = item.get(
            "low_stock_threshold",
            5
        )

        if item["quantity"] <= threshold:

            alert_message = (
                f"{item['name']} stock is running low"
            )

            notifications_collection.insert_one({

                "user_email": admin["email"],

                "title": "Low Stock Alert",

                "message": alert_message,

                "notification_type": "inventory",

                "is_read": False,

                "created_at": datetime.utcnow()
            })

            alerts.append(alert_message)

    return {
        "alerts": alerts
    }


# =====================================
# INVENTORY LOGS
# =====================================
@router.get("/logs")
def inventory_logs(
    admin: dict = Depends(admin_required)
):

    logs = list(
        inventory_logs_collection.find()
    )

    for log in logs:

        log["_id"] = str(log["_id"])

    return logs