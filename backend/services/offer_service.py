from database import (
    offers_collection
)


# =====================================
# GET ACTIVE OFFERS
# =====================================
def get_active_offers_service():

    offers = list(
        offers_collection.find()
    )

    for offer in offers:

        offer["_id"] = str(offer["_id"])

    return offers