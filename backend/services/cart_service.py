from database import (
    cart_collection
)


# =====================================
# CALCULATE CART TOTAL
# =====================================
def calculate_cart_total(
    user_email: str
):

    cart_items = list(
        cart_collection.find({
            "user_email": user_email
        })
    )

    total_amount = 0

    for item in cart_items:

        subtotal = (
            item["price"]
            * item["quantity"]
        )

        total_amount += subtotal

    return total_amount


# =====================================
# GET USER CART
# =====================================
def get_user_cart_service(
    user_email: str
):

    cart_items = list(
        cart_collection.find({
            "user_email": user_email
        })
    )

    for item in cart_items:

        item["_id"] = str(item["_id"])

    return cart_items