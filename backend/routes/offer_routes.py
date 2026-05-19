from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime

from database import (
    items_collection,
    offers_collection
)

from middleware.auth_middleware import (
    admin_required
)

from models.offer_model import OfferModel

router = APIRouter(
    prefix="/offers",
    tags=["Offers"]
)


# =====================================
# CREATE OFFER
# =====================================
@router.post("/create")
def create_offer(
    offer: OfferModel,
    admin: dict = Depends(admin_required)
):

    item = items_collection.find_one({
        "_id": ObjectId(offer.item_id)
    })

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    offer_data = offer.dict()

    offer_data["created_at"] = datetime.utcnow()

    offers_collection.insert_one(
        offer_data
    )

    # UPDATE ITEM OFFER
    items_collection.update_one(
        {"_id": ObjectId(offer.item_id)},
        {
            "$set": {
                "offer_percentage": offer.discount_percentage
            }
        }
    )

    return {
        "message": "Offer created successfully"
    }


# =====================================
# GET ALL OFFERS
# =====================================
@router.get("/")
def get_all_offers():

    offers = list(
        offers_collection.find()
    )

    for offer in offers:

        offer["_id"] = str(offer["_id"])

    return offers


# =====================================
# APPLY OFFER TO ITEM
# =====================================
@router.put("/apply/{item_id}")
def apply_offer(
    item_id: str,
    data: dict,
    admin: dict = Depends(admin_required)
):

    discount = data.get(
        "discount_percentage"
    )

    if discount is None:

        raise HTTPException(
            status_code=400,
            detail="Discount percentage required"
        )

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$set": {
                "offer_percentage": discount
            }
        }
    )

    return {
        "message": "Offer applied successfully"
    }


# =====================================
# REMOVE OFFER
# =====================================
@router.put("/remove/{item_id}")
def remove_offer(
    item_id: str,
    admin: dict = Depends(admin_required)
):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {
            "$set": {
                "offer_percentage": 0
            }
        }
    )

    return {
        "message": "Offer removed successfully"
    }


# =====================================
# GET ITEM FINAL PRICE
# =====================================
@router.get("/final-price/{item_id}")
def get_final_price(item_id: str):

    item = items_collection.find_one({
        "_id": ObjectId(item_id)
    })

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    original_price = item["price"]

    discount = item.get(
        "offer_percentage",
        0
    )

    final_price = original_price - (
        original_price * discount / 100
    )

    return {

        "item_name": item["name"],

        "original_price": original_price,

        "discount_percentage": discount,

        "final_price": round(final_price, 2)
    }