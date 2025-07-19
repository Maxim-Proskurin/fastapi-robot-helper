import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    username = Column(
        String(30),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password = Column(
        String,
        nullable=False
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )