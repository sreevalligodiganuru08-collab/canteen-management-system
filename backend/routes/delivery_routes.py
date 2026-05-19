from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import (
    orders_collection,
    delivery_collection,
    delivery_tracking_collection,
    notifications_collection
)

from middleware.auth_middleware import (
    delivery_required,
    admin_required,
    get_current_user
)

router = APIRouter(
    prefix="/delivery",
    tags=["Delivery"]
)


# =====================================
# AVAILABLE ORDERS FOR DELIVERY
# =====================================
@router.get("/available-orders")
def available_orders(
    delivery: dict = Depends(delivery_required)
):

    city = delivery.get("city", "")
    area = delivery.get("area", "")

    orders = list(
        orders_collection.find({
            "status": "Ready For Pickup",
            "assigned_city": city,
            "assigned_area": area
        })
    )

    for order in orders:
        order["_id"] = str(order["_id"])

    return orders


# =====================================
# ACCEPT ORDER
# =====================================
@router.put("/accept-order/{order_id}")
def accept_order(
    order_id: str,
    delivery: dict = Depends(delivery_required)
):

    order = orders_collection.find_one({
        "_id": ObjectId(order_id)
    })

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {

                "delivery_partner_email": delivery["email"],

                "delivery_status": "Assigned",

                "status": "Out For Delivery"
            }
        }
    )

    # DELIVERY TRACKING ENTRY
    delivery_tracking_collection.insert_one({

        "order_id": order_id,

        "delivery_partner_email": delivery["email"],

        "current_status": "Assigned",

        "current_location": "",

        "destination_location": order.get(
            "user_location",
            ""
        ),

        "reached_destination": False,

        "delivered_successfully": False,

        "updated_at": datetime.utcnow()
    })

    # USER NOTIFICATION
    notifications_collection.insert_one({

        "user_email": order["user_email"],

        "title": "Delivery Assigned",

        "message": "Delivery partner assigned to your order",

        "notification_type": "delivery",

        "is_read": False,

        "created_at": datetime.utcnow()
    })

    return {
        "message": "Order accepted successfully"
    }


# =====================================
# MY DELIVERIES
# =====================================
@router.get("/my-orders")
def my_orders(
    delivery: dict = Depends(delivery_required)
):

    orders = list(
        orders_collection.find({
            "delivery_partner_email": delivery["email"]
        })
    )

    for order in orders:
        order["_id"] = str(order["_id"])

    return orders


# =====================================
# UPDATE DELIVERY STATUS
# =====================================
@router.put("/update-status/{order_id}")
def update_delivery_status(
    order_id: str,
    data: dict,
    delivery: dict = Depends(delivery_required)
):

    allowed_status = [

        "Picked Up",

        "Reached Location",

        "Waiting For Confirmation",

        "Delivered"
    ]

    status = data.get("status")

    if status not in allowed_status:

        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "delivery_status": status
            }
        }
    )

    delivery_tracking_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {
                "current_status": status,
                "updated_at": datetime.utcnow()
            }
        }
    )

    order = orders_collection.find_one({
        "_id": ObjectId(order_id)
    })

    # USER NOTIFICATION
    notifications_collection.insert_one({

        "user_email": order["user_email"],

        "title": "Delivery Update",

        "message": f"Your order is now {status}",

        "notification_type": "delivery",

        "is_read": False,

        "created_at": datetime.utcnow()
    })

    return {
        "message": f"Delivery status updated to {status}"
    }


# =====================================
# USER CONFIRM DELIVERY
# =====================================
@router.put("/confirm-delivery/{order_id}")
def confirm_delivery(
    order_id: str,
    data: dict,
    current_user: dict = Depends(get_current_user)
):

    order = orders_collection.find_one({
        "_id": ObjectId(order_id)
    })

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    # ONLY ORDER OWNER CAN CONFIRM
    if current_user["email"] != order["user_email"]:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    delivered = data.get("delivered")

    # USER CONFIRMED SUCCESS
    if delivered is True:

        orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "delivery_status": "Delivered",
                    "status": "Delivered"
                }
            }
        )

        return {
            "message": "Delivery confirmed successfully"
        }

    # USER REPORTED ISSUE
    else:

        orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {
                "$set": {
                    "delivery_issue": True,
                    "status": "Issue Reported"
                }
            }
        )

        return {
            "message": "Issue reported to admin"
        }

# =====================================
# DELIVERY TRACKING DETAILS
# =====================================
@router.get("/tracking/{order_id}")
def tracking_details(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):

    tracking = delivery_tracking_collection.find_one({
        "order_id": order_id
    })

    if not tracking:

        raise HTTPException(
            status_code=404,
            detail="Tracking not found"
        )

    tracking["_id"] = str(tracking["_id"])

    return tracking


# =====================================
# ALL DELIVERY PARTNERS (ADMIN)
# =====================================
@router.get("/partners")
def all_delivery_partners(
    admin: dict = Depends(admin_required)
):

    partners = list(
        delivery_collection.find()
    )

    for partner in partners:
        partner["_id"] = str(partner["_id"])

    return partners