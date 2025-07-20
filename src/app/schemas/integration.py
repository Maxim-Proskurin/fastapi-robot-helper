from pydantic import BaseModel, Field

class SendMessageRequest(BaseModel):
    """
    Схема для запроса на отправку сообщения через внешний API.
    """
    to: str = Field(..., description="Кому отправить (номер, email, chat_id и т.д.)")
    text: str = Field(..., description="Текст сообщения")
    api_url: str = Field(..., description="URL внешнего API")
    api_token: str | None = Field(default=None, description="Токен для авторизации (если требуется)")

class SendMessageResponse(BaseModel):
    """
    Схема для ответа от внешнего API (можно расширять под нужды).
    """
    status_code: int | None = Field(default=None, description="HTTP статус-код ответа внешнего API")
    error: str | None = Field(default=None, description="Ошибка, если есть")
    data: dict | None = Field(default=None, description="Данные ответа внешнего API")