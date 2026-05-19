from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import (
    payments_collection,
    orders_collection,
    notifications_collection
)

from middleware.auth_middleware import (
    admin_required,
    delivery_required,
    get_current_user
)

from models.payment_model import PaymentModel

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# =====================================
# CREATE PAYMENT
# =====================================
@router.post("/create")
def create_payment(
    payment: PaymentModel,
    current_user: dict = Depends(get_current_user)
):

    order = orders_collection.find_one({
        "_id": ObjectId(payment.order_id)
    })

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    existing_payment = payments_collection.find_one({
        "order_id": payment.order_id
    })

    if existing_payment:

        raise HTTPException(
            status_code=400,
            detail="Payment already exists"
        )

    payment_data = payment.dict()

    payment_data["user_email"] = current_user["email"]

    payment_data["payment_status"] = "Pending"

    payment_data["created_at"] = datetime.utcnow()

    result = payments_collection.insert_one(
        payment_data
    )

    return {

        "message": "Payment created successfully",

        "payment_id": str(result.inserted_id)
    }


# =====================================
# USER PAYMENT HISTORY
# =====================================
@router.get("/my-payments")
def my_payments(
    current_user: dict = Depends(get_current_user)
):

    payments = list(
        payments_collection.find({
            "user_email": current_user["email"]
        }).sort("created_at", -1)
    )

    for payment in payments:

        payment["_id"] = str(payment["_id"])

    return payments


# =====================================
# GET SINGLE PAYMENT
# =====================================
@router.get("/{payment_id}")
def get_payment(
    payment_id: str,
    current_user: dict = Depends(get_current_user)
):

    payment = payments_collection.find_one({
        "_id": ObjectId(payment_id)
    })

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payment["_id"] = str(payment["_id"])

    return payment


# =====================================
# UPLOAD COD PAYMENT PROOF
# =====================================
@router.put("/upload-proof/{order_id}")
def upload_payment_proof(
    order_id: str,
    data: dict,
    delivery: dict = Depends(delivery_required)
):

    payment = payments_collection.find_one({
        "order_id": order_id
    })

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payments_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {

                "payment_proof_image": data.get(
                    "payment_proof_image"
                ),

                "collected_amount": data.get(
                    "collected_amount"
                ),

                "collected_by": delivery["email"],

                "payment_status": "Verification Pending",

                "updated_at": datetime.utcnow()
            }
        }
    )

    # ADMIN NOTIFICATION
    notifications_collection.insert_one({

        "user_email": "admin",

        "title": "COD Verification Pending",

        "message": f"Delivery partner uploaded COD proof for order {order_id}",

        "notification_type": "payment",

        "is_read": False,

        "created_at": datetime.utcnow()
    })

    return {
        "message": "Payment proof uploaded successfully"
    }


# =====================================
# ADMIN VERIFY PAYMENT
# =====================================
@router.put("/verify/{order_id}")
def verify_payment(
    order_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    status = data.get("status")

    allowed_status = [

        "Verified",

        "Rejected"
    ]

    if status not in allowed_status:

        raise HTTPException(
            status_code=400,
            detail="Invalid payment status"
        )

    payment = payments_collection.find_one({
        "order_id": order_id
    })

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payments_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {

                "payment_status": status,

                "verified_by_admin": True,

                "updated_at": datetime.utcnow()
            }
        }
    )

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "payment_status": status
            }
        }
    )

    # USER NOTIFICATION
    notifications_collection.insert_one({

        "user_email": payment["user_email"],

        "title": "Payment Status Update",

        "message": f"Your payment has been {status}",

        "notification_type": "payment",

        "is_read": False,

        "created_at": datetime.utcnow()
    })

    return {
        "message": f"Payment {status}"
    }


# =====================================
# FAILED PAYMENT
# =====================================
@router.put("/fail/{order_id}")
def failed_payment(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):

    payment = payments_collection.find_one({
        "order_id": order_id
    })

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payments_collection.update_one(
        {"order_id": order_id},
        {
            "$set": {

                "payment_status": "Failed",

                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "message": "Payment marked as failed"
    }


# =====================================
# ALL PAYMENTS (ADMIN)
# =====================================
@router.get("/")
def all_payments(
    admin: dict = Depends(admin_required)
):

    payments = list(
        payments_collection.find()
        .sort("created_at", -1)
    )

    for payment in payments:

        payment["_id"] = str(payment["_id"])

    return payments


# =====================================
# PAYMENT ANALYTICS SUMMARY
# =====================================
@router.get("/summary/stats")
def payment_summary(
    admin: dict = Depends(admin_required)
):

    verified = payments_collection.count_documents({
        "payment_status": "Verified"
    })

    pending = payments_collection.count_documents({
        "payment_status": "Verification Pending"
    })

    failed = payments_collection.count_documents({
        "payment_status": "Failed"
    })

    rejected = payments_collection.count_documents({
        "payment_status": "Rejected"
    })

    return {

        "verified_payments": verified,

        "pending_verifications": pending,

        "failed_payments": failed,

        "rejected_payments": rejected
    }