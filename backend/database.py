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
users_collection = db["users"]

items_collection = db["items"]

cart_collection = db["cart"]

orders_collection = db["orders"]


print("MongoDB Connected Successfully")