import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.app.core.database import Base

class Script(Base):
    """
    Модель скрипта коммуникации.

    Атрибуты:
        id (UUID): Уникальный идентификатор скрипта.
        name (str): Название скрипта.
        content (str): Текст/контент скрипта.
        user_id (UUID): Владелец скрипта (FK на пользователя).
        created_at (datetime): Дата и время создания скрипта.
        updated_at (datetime): Дата и время последнего обновления скрипта.
    """
    __tablename__ = "scripts"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(
        String(100),
        nullable=False
    )
    content = Column(
        String,
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )