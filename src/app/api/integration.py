import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from src.app.depends.auth import get_current_user_id
from src.app.schemas.integration import SendMessageRequest, SendMessageResponse
from src.app.service.integration import ExternalMessenger

router = APIRouter(prefix="/integration", tags=["integration"])


@router.post("/send_message", response_model=SendMessageResponse)
async def send_message(
    data: SendMessageRequest, user_id: UUID = Depends(get_current_user_id)
):
    """
    Отправить сообщение через внешний API (пример интеграции).

    Требует авторизации через Bearer-токен (JWT).
    user_id автоматически извлекается из access_token.

    Args:
        data (SendMessageRequest): Данные для отправки сообщения.

    Returns:
        dict: Ответ от внешнего API или ошибка.
    """
    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)
    result = await ExternalMessenger.send_message(
        to=data.to, text=data.text, api_url=data.api_url, api_token=data.api_token
    )
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Ошибка внешнего API: {result['error']}",
        )
    return result
