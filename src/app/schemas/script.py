from pydantic import BaseModel, Field
from uuid import UUID


class ScriptBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )
    content: str
    
class ScriptRead(ScriptBase):
    id: UUID

    model_config = {"from_attributes": True}
    