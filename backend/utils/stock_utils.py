# =====================================
# CHECK STOCK AVAILABILITY
# =====================================
def check_stock_availability(
    available_quantity,
    requested_quantity
):

    return available_quantity >= requested_quantity


# =====================================
# LOW STOCK CHECK
# =====================================
def is_low_stock(
    quantity,
    threshold=5
):

    return quantity <= threshold


# =====================================
# SOLD PERCENTAGE
# =====================================
def calculate_sold_percentage(
    total_stock,
    remaining_stock
):

    sold = total_stock - remaining_stock

    return round(
        (sold / total_stock) * 100,
        2
    )