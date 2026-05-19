from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import notifications_collection

from middleware.auth_middleware import (
    get_current_user,
    admin_required
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# =====================================
# SEND NOTIFICATION
# =====================================
@router.post("/send")
def send_notification(
    data: dict,
    admin: dict = Depends(admin_required)
):

    required_fields = [

        "user_email",

        "title",

        "message",

        "notification_type"
    ]

    for field in required_fields:

        if field not in data:

            raise HTTPException(
                status_code=400,
                detail=f"{field} is required"
            )

    notification_data = {

        "user_email": data["user_email"],

        "title": data["title"],

        "message": data["message"],

        "notification_type": data[
            "notification_type"
        ],

        "is_read": False,

        "created_at": datetime.utcnow()
    }

    notifications_collection.insert_one(
        notification_data
    )

    return {
        "message": "Notification sent successfully"
    }


# =====================================
# GET MY NOTIFICATIONS
# =====================================
@router.get("/my")
def my_notifications(
    current_user: dict = Depends(get_current_user)
):

    notifications = list(
        notifications_collection.find({
            "user_email": current_user["email"]
        }).sort("created_at", -1)
    )

    for notification in notifications:

        notification["_id"] = str(
            notification["_id"]
        )

    return notifications


# =====================================
# MARK NOTIFICATION AS READ
# =====================================
@router.put("/read/{notification_id}")
def mark_as_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):

    notification = notifications_collection.find_one({
        "_id": ObjectId(notification_id)
    })

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    if notification["user_email"] != current_user["email"]:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    notifications_collection.update_one(
        {"_id": ObjectId(notification_id)},
        {
            "$set": {
                "is_read": True
            }
        }
    )

    return {
        "message": "Notification marked as read"
    }


# =====================================
# DELETE NOTIFICATION
# =====================================
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):

    notification = notifications_collection.find_one({
        "_id": ObjectId(notification_id)
    })

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    if notification["user_email"] != current_user["email"]:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    notifications_collection.delete_one({
        "_id": ObjectId(notification_id)
    })

    return {
        "message": "Notification deleted successfully"
    }


# =====================================
# UNREAD NOTIFICATION COUNT
# =====================================
@router.get("/unread-count")
def unread_count(
    current_user: dict = Depends(get_current_user)
):

    count = notifications_collection.count_documents({

        "user_email": current_user["email"],

        "is_read": False
    })

    return {
        "unread_notifications": count
    }


# =====================================
# ADMIN ALL NOTIFICATIONS
# =====================================
@router.get("/all")
def all_notifications(
    admin: dict = Depends(admin_required)
):

    notifications = list(
        notifications_collection.find()
        .sort("created_at", -1)
    )

    for notification in notifications:

        notification["_id"] = str(
            notification["_id"]
        )

    return notifications