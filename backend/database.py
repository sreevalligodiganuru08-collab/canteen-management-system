from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)

db = client["canteen_db"]

users_collection = db["users"]
items_collection = db["items"]
orders_collection = db["orders"]

print("MongoDB Connected Successfully")