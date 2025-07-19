from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.user import UserCreate, UserLogin, UserRead
from src.app.service.user import UserService
from src.app.database import get_db

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
    return {
        "message": "Успешный вход.",
        "user_id": str(user.id)
    }