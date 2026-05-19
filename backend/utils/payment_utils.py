import uuid


# =====================================
# GENERATE PAYMENT ID
# =====================================
def generate_payment_id():

    return f"PAY-{uuid.uuid4().hex[:10].upper()}"


# =====================================
# VALIDATE PAYMENT AMOUNT
# =====================================
def validate_payment_amount(
    expected_amount,
    paid_amount
):

    return expected_amount == paid_amount


# =====================================
# PAYMENT STATUS CHECK
# =====================================
def is_payment_verified(
    payment_status
):

    return payment_status == "Verified"