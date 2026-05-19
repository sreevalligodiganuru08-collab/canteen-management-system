from jose import jwt

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# =====================================
# GENERATE ACCESS TOKEN
# =====================================
def generate_access_token(
    email,
    role
):

    payload = {

        "sub": email,

        "role": role
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token