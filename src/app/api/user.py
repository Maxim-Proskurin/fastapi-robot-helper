from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.database import get_db
from src.app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserLogin, UserRead, UserUpdate
from src.app.service.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=201
)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Зарегистрировать нового пользователя.

    Args:
        user_data (UserCreate):
        Данные для создания пользователя.
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        UserRead: Данные зарегистрированного пользователя.

    Raises:
        HTTPException:
        Если пользователь с таким email или username уже существует.
    """
    user, error = await UserService.create_user(user_data, db)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error or "Ошибка аутентификации",
        )
    return user


@router.post("/login")
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация пользователя и выдача access/refresh токенов.

    Args:
        login_data (UserLogin): Данные для входа (email и пароль).
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        dict: access_token, refresh_token, token_type, message

    Raises:
        HTTPException: Если неверный email или пароль.
    """
    user, error = await UserService.authenticate_user(login_data, db)
    if error or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error or "Ошибка аутентификации",
        )
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Успешный вход.",
    }


@router.post("/refresh")
async def refresh_token_endpoints(refresh_token: str):
    """
    Обновить access и refresh токены по refresh-токену.

    Args:
        refresh_token (str): Валидный refresh-токен.

    Returns:
        dict: Новый access_token, refresh_token, token_type

    Raises:
        HTTPException: Если refresh-токен невалиден.
    """
    payload = decode_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен",
        )
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Получить пользователя по id.

    Args:
        user_id (str): UUID пользователя.
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
    UserRead: Данные пользователя.
    Raises:
        HTTPException: Если пользователь не найден.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    if user := result.scalar_one_or_none():
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден."
        )


@router.get("/", response_model=list[UserRead])
async def list_users(
    db: AsyncSession = Depends(get_db),
):
    """
    Получить список всех пользователей.

    Args:
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        list[UserRead]: Список пользователей.
    """
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID, user_data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Обновить данные пользователя (только full_name и/или пароль).

    Args:
        user_id (str): UUID пользователя.
        user_data (UserUpdate): Новые данные пользователя.
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        UserRead: Обновлённые данные пользователя.

    Raises:
        HTTPException: Если пользователь не найден.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
            )
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        setattr(
            user,
            "hashed_password",
            pwd_context.hash(update_data.pop("password"))
        )
    for field, value in update_data.items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Удалить пользователя по id.
    Args:
        user_id (str): UUID пользователя.
        db (AsyncSession): Асинхронная сессия БД.
    Returns:
        None
    Raises:
        HTTPException: Если пользователь не найден.
    """
    result = await db.execute(
        select(User)
        .where(User.id == user_id)
        )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    await db.delete(user)
    await db.commit()
    return None, "Пользователь удален."
