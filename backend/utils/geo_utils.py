from math import radians, cos, sin, asin, sqrt


# =====================================
# CALCULATE DISTANCE
# =====================================
def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    # Haversine Formula

    lon1 = radians(lon1)
    lon2 = radians(lon2)

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    r = 6371

    return c * r


# =====================================
# CHECK DELIVERY RANGE
# =====================================
def within_delivery_range(
    distance,
    max_distance=10
):

    return distance <= max_distance