from pymongo import MongoClient


# =====================================
# MONGODB CONNECTION
# =====================================
MONGO_URL = "mongodb+srv://healthuser:healthpass123@cluster0.jrk94p8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["canteen_management"]


# =====================================
# COLLECTIONS
# =====================================

# USERS
users_collection = db["users"]

# MENU ITEMS
items_collection = db["menu"]

# CART
cart_collection = db["cart"]

# ORDERS
orders_collection = db["orders"]

# PAYMENTS
payments_collection = db["payments"]

# DELIVERY PARTNERS
delivery_collection = db["delivery"]

# DELIVERY TRACKING
delivery_tracking_collection = db["delivery_tracking"]

# NOTIFICATIONS
notifications_collection = db["notifications"]

# OFFERS
offers_collection = db["offers"]

# COMBOS
combos_collection = db["combos"]


print("MongoDB Connected Successfully")