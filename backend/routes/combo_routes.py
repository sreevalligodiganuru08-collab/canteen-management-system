from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import (
    combos_collection,
    items_collection
)

from middleware.auth_middleware import (
    admin_required
)

router = APIRouter(
    prefix="/combos",
    tags=["Combos"]
)


# =====================================
# CREATE COMBO
# =====================================
@router.post("/create")
def create_combo(
    data: dict,
    admin: dict = Depends(admin_required)
):

    required_fields = [

        "combo_name",

        "items",

        "combo_price",

        "image_path"
    ]

    for field in required_fields:

        if field not in data:

            raise HTTPException(
                status_code=400,
                detail=f"{field} is required"
            )

    total_original_price = 0

    combo_items = []

    for item_id in data["items"]:

        item = items_collection.find_one({
            "_id": ObjectId(item_id)
        })

        if not item:

            raise HTTPException(
                status_code=404,
                detail=f"Item {item_id} not found"
            )

        total_original_price += item["price"]

        combo_items.append({

            "item_id": str(item["_id"]),

            "name": item["name"],

            "price": item["price"],

            "image_path": item.get(
                "image_path",
                ""
            )
        })

    discount_percentage = round(

        (
            (
                total_original_price
                - data["combo_price"]
            )
            / total_original_price
        ) * 100,
        2
    )

    combo_data = {

        "combo_name": data["combo_name"],

        "items": combo_items,

        "original_price": total_original_price,

        "combo_price": data["combo_price"],

        "discount_percentage": discount_percentage,

        "image_path": data["image_path"],

        "available": True,

        "created_by": admin["email"],

        "created_at": datetime.utcnow()
    }

    result = combos_collection.insert_one(
        combo_data
    )

    return {

        "message": "Combo created successfully",

        "combo_id": str(result.inserted_id)
    }


# =====================================
# GET ALL COMBOS
# =====================================
@router.get("/")
def get_all_combos():

    combos = list(
        combos_collection.find()
    )

    for combo in combos:

        combo["_id"] = str(combo["_id"])

    return combos


# =====================================
# GET SINGLE COMBO
# =====================================
@router.get("/{combo_id}")
def get_combo(combo_id: str):

    combo = combos_collection.find_one({
        "_id": ObjectId(combo_id)
    })

    if not combo:

        raise HTTPException(
            status_code=404,
            detail="Combo not found"
        )

    combo["_id"] = str(combo["_id"])

    return combo


# =====================================
# UPDATE COMBO
# =====================================
@router.put("/update/{combo_id}")
def update_combo(
    combo_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    combo = combos_collection.find_one({
        "_id": ObjectId(combo_id)
    })

    if not combo:

        raise HTTPException(
            status_code=404,
            detail="Combo not found"
        )

    combos_collection.update_one(
        {"_id": ObjectId(combo_id)},
        {
            "$set": data
        }
    )

    return {
        "message": "Combo updated successfully"
    }


# =====================================
# DELETE COMBO
# =====================================
@router.delete("/delete/{combo_id}")
def delete_combo(
    combo_id: str,
    admin: dict = Depends(admin_required)
):

    combo = combos_collection.find_one({
        "_id": ObjectId(combo_id)
    })

    if not combo:

        raise HTTPException(
            status_code=404,
            detail="Combo not found"
        )

    combos_collection.delete_one({
        "_id": ObjectId(combo_id)
    })

    return {
        "message": "Combo deleted successfully"
    }


# =====================================
# AVAILABLE COMBOS
# =====================================
@router.get("/available/list")
def available_combos():

    combos = list(
        combos_collection.find({
            "available": True
        })
    )

    for combo in combos:

        combo["_id"] = str(combo["_id"])

    return combos