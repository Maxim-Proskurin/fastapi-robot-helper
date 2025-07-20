from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator
)
from uuid import UUID
from datetime import datetime
import re

class UserCreate(BaseModel):
    """
    Схема для создания пользователя.
    """
    username: str = Field(min_length=5, max_length=30)
    password: str = Field(min_length=6, max_length=128)
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100)
    
    @field_validator("username")
    @classmethod
    def username_no_spaces(cls, v):
        if " " in v:
            raise ValueError("Имя пользователя не должно содержать пробелов.")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну букву.")
        if not re.search(r"[!@#$%^&*(),.?\\/:;{}|><\[\]]", v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол.")
        easy_password = [
            "password",
            "123456",
            "qwerty",
            "admin",
            "abc123",
            "111111",
            "123123",
            "321321"
        ]
        for easy in easy_password:
            if easy in v.lower():
                raise ValueError("Пароль слишком простой!")
        return v

class UserRead(BaseModel):
    """
    Схема для чтения пользователя (response).
    """
    id: UUID
    username: str
    full_name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None = None
    last_login: datetime | None = None
    
    model_config = {"from_attributes": True}
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    password: str | None = Field(default=None, min_length=6, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну букву.")
        if not re.search(r"[!@#$%^&*(),.?\\/:;{}|><\[\]]", v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол.")
        easy_password = [
            "password",
            "123456",
            "qwerty",
            "admin",
            "abc123",
            "111111",
            "123123",
            "321321"
        ]
        for easy in easy_password:
            if easy in v.lower():
                raise ValueError("Пароль слишком простой!")
        return v