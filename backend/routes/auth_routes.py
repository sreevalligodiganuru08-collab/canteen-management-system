from fastapi import APIRouter, HTTPException
from database import users_collection

from models.user_model import UserSignup, UserLogin

from config.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

# Signup
@router.post("/signup")
def signup(user: UserSignup):

    # Check existing email
    existing_email = users_collection.find_one({
        "email": user.email
    })

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Check existing phone
    existing_phone = users_collection.find_one({
        "phone": user.phone
    })

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone already exists"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "password": hashed_password,
        "role": user.role
    }

    users_collection.insert_one(user_data)

    token = create_access_token({
        "email": user.email,
        "role": user.role
    })

    return {
        "message": "User created successfully",
        "access_token": token,
        "token_type": "bearer"
    }

# Login
@router.post("/login")
def login(user: UserLogin):

    existing_user = users_collection.find_one({
        "$or": [
            {"email": user.login_id},
            {"phone": user.login_id}
        ]
    })

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    valid_password = verify_password(
        user.password,
        existing_user["password"]
    )

    if not valid_password:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "email": existing_user["email"],
        "role": existing_user["role"]
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "name": existing_user["name"],
            "email": existing_user["email"],
            "role": existing_user["role"]
        }
    }