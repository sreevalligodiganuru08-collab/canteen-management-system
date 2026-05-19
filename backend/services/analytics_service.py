from database import (
    orders_collection
)


# =====================================
# TOTAL REVENUE
# =====================================
def calculate_total_revenue():

    orders = list(
        orders_collection.find()
    )

    revenue = 0

    for order in orders:

        revenue += order.get(
            "total_amount",
            0
        )

    return revenue