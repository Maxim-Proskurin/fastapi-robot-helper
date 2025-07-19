from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt,  JWTError
from src.app.core.config import settings

ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(
    data: dict[str, Any],
    expires_delta: int | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_access_token(
    token:str
) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except JWTError:
        return {}
    
def create_refresh_token(
    data: dict[str, Any],
    expires_delta: int | None = None
) -> str:
    refresh_expire_minutes = expires_delta or settings.REFRESH_TOKEN_EXPIRE_MINUTES
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=refresh_expire_minutes
    )
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_refresh_token(
    token: str
) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=ALGORITHM
        )
        return payload
    except JWTError:
        return {}