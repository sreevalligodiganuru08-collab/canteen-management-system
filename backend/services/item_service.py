from bson import ObjectId

from database import (
    items_collection
)


# =====================================
# GET ALL ITEMS
# =====================================
def get_all_items_service():

    items = list(
        items_collection.find()
    )

    for item in items:

        item["_id"] = str(item["_id"])

    return items


# =====================================
# GET SINGLE ITEM
# =====================================
def get_single_item_service(item_id: str):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if item:

        item["_id"] = str(item["_id"])

    return item


# =====================================
# UPDATE STOCK
# =====================================
def update_item_stock(
    item_id: str,
    quantity: int
):

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$inc": {
                "quantity": -quantity,
                "sold_count": quantity
            }
        }
    )


# =====================================
# RESTORE STOCK
# =====================================
def restore_item_stock(
    item_id: str,
    quantity: int
):

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$inc": {
                "quantity": quantity
            }
        }
    )