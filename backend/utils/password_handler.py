from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str):
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*_)[A-Za-z\d_]{8,}$'

    if not re.match(pattern, password):
        return False

    return True

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)