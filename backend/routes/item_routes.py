from fastapi import APIRouter, HTTPException, Depends, Query
from bson import ObjectId
from database import items_collection
from models.item_model import ItemCreate, ItemUpdate
from middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

# ==============================
# ADD ITEM (ADMIN ONLY)
# ==============================
@router.post("/")
def add_item(item: ItemCreate, current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add items")

    new_item = {
        "name": item.name,
        "price": item.price,
        "quantity": item.quantity,
        "category": item.category,
        "image_path": item.image_path,
        "description": item.description,
        "available": True
    }

    result = items_collection.insert_one(new_item)

    return {
        "message": "Item added successfully",
        "item_id": str(result.inserted_id)
    }


# ==============================
# GET ALL ITEMS
# ==============================
@router.get("/")
def get_items(
    search: str = Query(default=""),
    category: str = Query(default="")
):

    query = {}

    # Search by name
    if search:
        query["name"] = {
            "$regex": search,
            "$options": "i"
        }

    # Filter category
    if category:
        query["category"] = category

    items = list(items_collection.find(query))

    formatted_items = []

    for item in items:
        formatted_items.append({
            "id": str(item["_id"]),
            "name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "category": item["category"],
            "image_path": item.get("image_path", ""),
            "description": item.get("description", ""),
            "available": item.get("available", True)
        })

    return formatted_items


# ==============================
# GET SINGLE ITEM
# ==============================
@router.get("/{item_id}")
def get_single_item(item_id: str):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "price": item["price"],
        "quantity": item["quantity"],
        "category": item["category"],
        "image_path": item.get("image_path", ""),
        "description": item.get("description", ""),
        "available": item.get("available", True)
    }


# ==============================
# UPDATE ITEM
# ==============================
@router.put("/{item_id}")
def update_item(
    item_id: str,
    item: ItemUpdate,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update items")

    existing_item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_data = {
        k: v
        for k, v in item.dict().items()
        if v is not None
    }

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": updated_data}
    )

    return {
        "message": "Item updated successfully"
    }


# ==============================
# DELETE ITEM
# ==============================
@router.delete("/{item_id}")
def delete_item(
    item_id: str,
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete items")

    existing_item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    items_collection.delete_one({
        "_id": ObjectId(item_id)
    })

    return {
        "message": "Item deleted successfully"
    }