from database import (
    users_collection,
    orders_collection,
    items_collection
)


# =====================================
# DASHBOARD COUNTS
# =====================================
def dashboard_counts():

    return {

        "users": users_collection.count_documents({
            "role": "user"
        }),

        "delivery_partners": users_collection.count_documents({
            "role": "delivery"
        }),

        "orders": orders_collection.count_documents({}),

        "items": items_collection.count_documents({})
    }