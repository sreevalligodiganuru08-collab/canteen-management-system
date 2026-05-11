from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

client = AsyncIOMotorClient(settings.MONGO_URI)

database = client[settings.DATABASE_NAME]

users_collection = database["users"]
items_collection = database["items"]
orders_collection = database["orders"]