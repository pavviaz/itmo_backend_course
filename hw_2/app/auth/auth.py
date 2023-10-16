from datetime import timedelta, datetime

from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException, status

from app.settings import JWT_SECRET, ALGORITHM, TOKEN_EXPIRE_TIME


pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, ALGORITHM)
    return encoded_jwt


def validate_access_token(token: str) -> str:
    try:
        token_data = jwt.decode(token, JWT_SECRET, ALGORITHM)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad token"
        )

    return token_data["sub"]
