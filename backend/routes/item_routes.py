from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId

from database import items_collection
from models.item_model import ItemCreate, ItemUpdate
from middleware.auth_middleware import admin_required

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


# ==========================================
# ADD ITEM (ADMIN ONLY)
# ==========================================
@router.post("/add")
def add_item(
    item: ItemCreate,
    admin: dict = Depends(admin_required)
):

    item_data = item.dict()

    result = items_collection.insert_one(item_data)

    return {
        "message": "Item added successfully",
        "item_id": str(result.inserted_id)
    }


# ==========================================
# GET ALL ITEMS
# ==========================================
@router.get("/")
def get_all_items():

    items = []

    for item in items_collection.find():

        item["_id"] = str(item["_id"])

        items.append(item)

    return items


# ==========================================
# GET SINGLE ITEM
# ==========================================
@router.get("/{item_id}")
def get_single_item(item_id: str):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item["_id"] = str(item["_id"])

    return item


# ==========================================
# UPDATE ITEM (ADMIN ONLY)
# ==========================================
@router.put("/update/{item_id}")
def update_item(
    item_id: str,
    updated_data: ItemUpdate,
    admin: dict = Depends(admin_required)
):

    result = items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$set": updated_data.dict(exclude_none=True)
        }
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not updated"
        )

    return {
        "message": "Item updated successfully"
    }


# ==========================================
# DELETE ITEM (ADMIN ONLY)
# ==========================================
@router.delete("/delete/{item_id}")
def delete_item(
    item_id: str,
    admin: dict = Depends(admin_required)
):

    result = items_collection.delete_one({
        "_id": ObjectId(item_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "message": "Item deleted successfully"
    }