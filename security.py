import os
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
load_dotenv()

# this will hash the password
password_hash = PasswordHash.recommended()

# this is for JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing in .env")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token