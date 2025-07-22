import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.app.core.database import Base


class User(Base):
    """
    Модель пользователя для хранения в базе данных.

    Атрибуты:
        id (UUID): Уникальный идентификатор пользователя.
        username (str): Уникальное имя пользователя (до 30 символов).
        full_name (str): Полное имя пользователя (опционально).
        hashed_password (str): Хешированный пароль пользователя.
        email (str): Уникальный email пользователя.
        is_active (bool): Активен ли пользователь.
        is_superuser (bool): Является ли пользователь админом.
        created_at (datetime): Дата и время создания пользователя.
        updated_at (datetime): Дата и время последнего обновления профиля.
        last_login (datetime): Дата и время последнего входа.
    """

    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(
        String(30),
        unique=True,
        index=True,
        nullable=False
    )
    full_name = Column(
        String(100),
        nullable=False,
        default="",
        server_default=""
    )
    hashed_password = Column(String, nullable=False)
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    is_active = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="1"
    )
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
    last_login = Column(DateTime(timezone=True), nullable=True)
