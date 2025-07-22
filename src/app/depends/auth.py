from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", auto_error=True)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    print("TOKEN:", token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (no token provided)",
        )
    payload = decode_access_token(token)
    print("PAYLOAD:", payload)
    if user_id := payload.get("sub"):
        return UUID(user_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось получить user_id из токена",
    )
