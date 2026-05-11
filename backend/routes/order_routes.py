from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from database import orders_collection

router = APIRouter()


# -------------------------------
# Helper: Serialize MongoDB
# -------------------------------
def serialize_order(order):
    order["_id"] = str(order["_id"])
    return order


# -------------------------------
# PLACE ORDER (CUSTOMER)
# -------------------------------
@router.post("/orders/place")
def place_order(order: dict):

    email = order.get("email")
    items = order.get("items")

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    if not items or len(items) == 0:
        raise HTTPException(status_code=400, detail="Items cannot be empty")

    new_order = {
        "email": email,
        "items": items,
        "status": "Pending",
        "created_at": datetime.utcnow()
    }

    result = orders_collection.insert_one(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": str(result.inserted_id)
    }


# -------------------------------
# GET USER ORDERS
# -------------------------------
@router.get("/orders/user/{email}")
def get_user_orders(email: str):

    orders = orders_collection.find({"email": email})

    return [serialize_order(order) for order in orders]


# -------------------------------
# GET ALL ORDERS (ADMIN)
# -------------------------------
@router.get("/orders/all")
def get_all_orders():

    orders = orders_collection.find()

    return [serialize_order(order) for order in orders]


# -------------------------------
# UPDATE ORDER STATUS (ADMIN)
# -------------------------------
@router.put("/orders/update-status/{order_id}")
def update_order_status(order_id: str, data: dict):

    status = data.get("status")

    valid_statuses = ["Pending", "Preparing", "Completed", "Cancelled"]

    if not status:
        raise HTTPException(status_code=400, detail="Status is required")

    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": f"Order updated to {status}"}