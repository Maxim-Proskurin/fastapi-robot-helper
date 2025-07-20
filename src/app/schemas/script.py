from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class ScriptCreate(BaseModel):
    """
    Схема для создания скрипта.
    """
    name: str = Field(
        min_length=1,
        max_length=100
    )
    content: str
    
class ScriptRead(BaseModel):
    """
    Схема для чтения скрипта (response).
    """
    id: UUID
    name: str
    content: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ScriptUpdate(BaseModel):
    """
    Схема для обновления скрипта.
    """
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
        )
    content: str | None = None