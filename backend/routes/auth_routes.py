from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import users_collection

from models.user_model import (
    UserSignup
)

from passlib.context import CryptContext
from jose import jwt

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    tags=["Authentication"]
)

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
# SIGNUP
# =====================================
@router.post("/signup")
def signup(user: UserSignup):

    existing_email = users_collection.find_one({
        "email": user.email
    })

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    existing_phone = users_collection.find_one({
        "phone": user.phone
    })

    if existing_phone:

        raise HTTPException(
            status_code=400,
            detail="Phone already exists"
        )

    user_dict = user.dict()

    user_dict["password"] = hash_password(
        user.password
    )

    users_collection.insert_one(user_dict)

    return {
        "message": "User created successfully"
    }


# =====================================
# LOGIN
# =====================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_collection.find_one({
        "$or": [
            {"email": form_data.username},
            {"phone": form_data.username}
        ]
    })

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    # TOKEN DATA
    token_data = {
        "sub": user["email"],
        "role": user["role"]
    }

    token = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "user": {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }