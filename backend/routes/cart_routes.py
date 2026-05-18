from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from database import cart_collection

from models.cart_model import CartModel

from middleware.auth_middleware import (
    get_current_user
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


# =====================================
# ADD TO CART
# =====================================
@router.post("/add")
def add_to_cart(
    cart: CartModel,
    current_user: dict = Depends(get_current_user)
):

    # USER ACCESS ONLY
    if current_user["role"] != "user":

        raise HTTPException(
            status_code=403,
            detail="Only users can access cart"
        )

    existing_item = cart_collection.find_one({
        "user_email": cart.user_email,
        "item_id": cart.item_id
    })

    # UPDATE QUANTITY
    if existing_item:

        new_quantity = (
            existing_item["quantity"]
            + cart.quantity
        )

        cart_collection.update_one(
            {
                "_id": existing_item["_id"]
            },
            {
                "$set": {
                    "quantity": new_quantity
                }
            }
        )

        return {
            "message": "Cart updated successfully"
        }

    # NEW CART ITEM
    cart_collection.insert_one(
        cart.dict()
    )

    return {
        "message": "Item added to cart"
    }


# =====================================
# GET USER CART
# =====================================
@router.get("/{email}")
def get_user_cart(
    email: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["email"] != email:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized access"
        )

    cart_items = list(
        cart_collection.find({
            "user_email": email
        })
    )

    for item in cart_items:
        item["_id"] = str(item["_id"])

    return cart_items


# =====================================
# REMOVE CART ITEM
# =====================================
@router.delete("/remove/{cart_id}")
def remove_cart_item(
    cart_id: str,
    current_user: dict = Depends(get_current_user)
):

    result = cart_collection.delete_one({
        "_id": ObjectId(cart_id)
    })

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    return {
        "message": "Item removed from cart"
    }


# =====================================
# CLEAR CART
# =====================================
@router.delete("/clear/{email}")
def clear_cart(
    email: str,
    current_user: dict = Depends(get_current_user)
):

    cart_collection.delete_many({
        "user_email": email
    })

    return {
        "message": "Cart cleared successfully"
    }