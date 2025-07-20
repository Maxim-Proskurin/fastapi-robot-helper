from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from src.app.api.user import get_current_user_id
from uuid import UUID
from src.app.service.integration import ExternalMessenger
from src.app.schemas.integration import SendMessageRequest, SendMessageResponse



router = APIRouter(prefix="/integration", tags=["integration"])





@router.post("/send_message", response_model=SendMessageResponse)
async def send_message(
    data: SendMessageRequest,
    user_id: UUID = Depends(get_current_user_id)
):
    """
    Отправить сообщение через внешний API (пример интеграции).

    Args:
        data (SendMessageRequest): Данные для отправки сообщения.
        user_id (UUID): Идентификатор пользователя (для логирования/аудита).

    Returns:
        SendMessageResponse: Ответ от внешнего API или ошибка.
    """
    result = await ExternalMessenger.send_message(
        to=data.to,
        text=data.text,
        api_url=data.api_url,
        api_token=data.api_token
    )
    if "error" in result:
        return SendMessageResponse(
            status_code=result.get("status_code"),
            error=result["error"],
            data=None
        )
    return SendMessageResponse(
        status_code=200,
        error=None,
        data=result
    )