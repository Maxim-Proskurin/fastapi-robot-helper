from pydantic import BaseModel, Field

class RegexpTextRequest(BaseModel):
    text: str = Field(..., description="Текст скрипта для анализа")

class RegexpPatternRequest(BaseModel):
    text: str = Field(..., description="Текст скрипта для проверки")
    pattern: str = Field(..., description="Регулярное выражение")
