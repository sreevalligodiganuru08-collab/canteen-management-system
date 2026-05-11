from fastapi import APIRouter, HTTPException
from database import users_collection
from models.user_model import UserSignup, UserLogin
from utils.hash import hash_password, verify_password
from utils.jwt_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Signup
@router.post("/signup")
def signup(user: UserSignup):

    existing_user = users_collection.find_one({
        "$or": [
            {"email": user.email},
            {"phone": user.phone}
        ]
    })

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)

    user_data = {
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "password": hashed_pw,
        "role": user.role
    }

    users_collection.insert_one(user_data)

    token = create_access_token({
        "email": user.email,
        "role": user.role
    })

    return {
        "success": True,
        "message": "Signup successful",
        "access_token": token
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
        raise HTTPException(status_code=404, detail="User not found")

    valid_password = verify_password(
        user.password,
        existing_user["password"]
    )

    if not valid_password:
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "email": existing_user["email"],
        "role": existing_user["role"]
    })

    return {
        "success": True,
        "message": "Login successful",
        "access_token": token,
        "role": existing_user["role"]
    }