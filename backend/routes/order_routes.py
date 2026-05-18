from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
import random

from database import (
    orders_collection,
    cart_collection
)

from middleware.auth_middleware import (
    get_current_user,
    admin_required
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# =====================================
# PLACE ORDER
# =====================================
@router.post("/place/{email}")
def place_order(
    email: str,
    payment_method: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["email"] != email:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    cart_items = list(cart_collection.find({
        "user_email": email
    }))

    if not cart_items:

        raise HTTPException(
            status_code=400,
            detail="Items cannot be empty"
        )

    total_amount = 0
    items = []

    for item in cart_items:

        subtotal = item["price"] * item["quantity"]

        total_amount += subtotal

        items.append({

            "item_id": item["item_id"],

            "name": item["name"],

            "price": item["price"],

            "quantity": item["quantity"],

            "image_path": item["image_path"],

            "subtotal": subtotal
        })

    pickup_token = str(random.randint(1000, 9999))

    order_data = {

        "user_email": email,

        "items": items,

        "total_amount": total_amount,

        "payment_method": payment_method,

        "payment_status": "Pending",

        "order_status": "Pending",

        "pickup_token": pickup_token,

        "estimated_time": "15 mins",

        "created_at": datetime.utcnow(),

        "delivered_at": None
    }

    result = orders_collection.insert_one(order_data)

    cart_collection.delete_many({
        "user_email": email
    })

    return {

        "message": "Order placed successfully",

        "order_id": str(result.inserted_id),

        "pickup_token": pickup_token,

        "estimated_time": "15 mins"
    }


# =====================================
# GET USER ORDERS
# =====================================
@router.get("/user/{email}")
def get_user_orders(
    email: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["email"] != email:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    orders = list(orders_collection.find({
        "user_email": email
    }))

    for order in orders:

        order["_id"] = str(order["_id"])

    return orders


# =====================================
# GET ALL ORDERS (ADMIN)
# =====================================
@router.get("/all")
def get_all_orders(
    admin: dict = Depends(admin_required)
):

    orders = list(orders_collection.find())

    for order in orders:

        order["_id"] = str(order["_id"])

    return orders


# =====================================
# UPDATE ORDER STATUS
# =====================================
@router.put("/status/{order_id}")
def update_order_status(
    order_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    allowed_status = [

        "Pending",

        "Preparing",

        "Ready",

        "Delivered",

        "Cancelled"
    ]

    status = data.get("status")

    if status not in allowed_status:

        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    update_data = {

        "order_status": status
    }

    if status == "Delivered":

        update_data["delivered_at"] = datetime.utcnow()

    result = orders_collection.update_one(

        {"_id": ObjectId(order_id)},

        {
            "$set": update_data
        }
    )

    if result.modified_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {

        "message": f"Order updated to {status}"
    }


# =====================================
# UPDATE PAYMENT STATUS
# =====================================
@router.put("/payment/{order_id}")
def update_payment_status(
    order_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    allowed_payment = [
        "Pending",
        "Paid",
        "Failed"
    ]

    payment_status = data.get("payment_status")

    if payment_status not in allowed_payment:

        raise HTTPException(
            status_code=400,
            detail="Invalid payment status"
        )

    result = orders_collection.update_one(

        {"_id": ObjectId(order_id)},

        {
            "$set": {
                "payment_status": payment_status
            }
        }
    )

    if result.modified_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {

        "message": f"Payment updated to {payment_status}"
    }