from database import (
    combos_collection
)


# =====================================
# GET ALL COMBOS
# =====================================
def get_all_combos_service():

    combos = list(
        combos_collection.find()
    )

    for combo in combos:

        combo["_id"] = str(combo["_id"])

    return combos