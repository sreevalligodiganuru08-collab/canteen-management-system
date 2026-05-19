from jose import jwt
from passlib.context import CryptContext

import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# =====================================
# HASH PASSWORD
# =====================================
def hash_password(password: str):

    return pwd_context.hash(password)


# =====================================
# VERIFY PASSWORD
# =====================================
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =====================================
# CREATE ACCESS TOKEN
# =====================================
def create_access_token(data: dict):

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )