from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.user import UserCreate, UserLogin, UserRead
from src.app.service.user import UserService
from src.app.core.database import get_db
from src.app.core.jwt import create_access_token, create_refresh_token, decode_refresh_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/register",
    response_model=UserRead,
    status_code=201)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user, error = await UserService.create_user(user_data, db)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error or "Ошибка аутентификации"
            )
    return user

@router.post("/login")
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user, error = await UserService.authenticate_user(login_data, db)
    if error or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error or "Ошибка аутентификации"
        )
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Успешный вход."
    }
    
@router.post("/refresh")
async def refresh_token_endpoints(refresh_token: str):
    payload = decode_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен"
        )
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }