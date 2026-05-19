from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from database import users_collection
from config.security import SECRET_KEY, ALGORITHM


# ==============================
# TOKEN SCHEMA
# ==============================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# ==============================
# GET CURRENT USER
# ==============================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = users_collection.find_one({
        "email": email
    })

    if user is None:
        raise credentials_exception

    user["_id"] = str(user["_id"])

    return user


# ==============================
# ADMIN REQUIRED
# ==============================

def admin_required(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


# ==============================
# DELIVERY REQUIRED
# ==============================

def delivery_required(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "delivery":

        raise HTTPException(
            status_code=403,
            detail="Delivery access required"
        )

    return current_user


# ==============================
# CUSTOMER REQUIRED
# ==============================

def customer_required(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "customer":

        raise HTTPException(
            status_code=403,
            detail="Customer access required"
        )

    return current_user