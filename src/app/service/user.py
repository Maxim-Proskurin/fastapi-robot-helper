from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.user import User
from src.app.schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    @staticmethod
    async def create_user(
        user_data: UserCreate, db: AsyncSession
    ) -> tuple[User | None, str | None]:
        """
        Создать нового пользователя.

        Args:
            user_data (UserCreate): Данные для создания пользователя.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            tuple[User | None, str | None]: Кортеж (пользователь, ошибка).
                Если пользователь успешно создан — (User, None).
                Если возникла ошибка — (None, сообщение об ошибке).
        """
        result_username = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        if result_username.scalar_one_or_none():
            return None, "Пользователь с таким именем существует."

        result_email = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        if result_email.scalar_one_or_none():
            return None, "Пользователь с таким email существует."

        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user, None

    @staticmethod
    async def authenticate_user(
        login_data: UserLogin, db: AsyncSession
    ) -> tuple[User | None, str | None]:
        """
        Аутентифицировать пользователя по email и паролю.

        Args:
            login_data (UserLogin): Данные для входа (email и пароль).
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            tuple[User | None, str | None]: Кортеж (пользователь, ошибка).
                Если аутентификация успешна — (User, None).
                Если неуспешна — (None, сообщение об ошибке).
        """
        result = await db.execute(
            select(User)
            .where(User.email == login_data.email
            )
        )
        user = result.scalar_one_or_none()
        if not user or not pwd_context.verify(
            login_data.password, getattr(user, "hashed_password", None)
        ):
            return None, "Неверный email или пароль."
        return user, None
