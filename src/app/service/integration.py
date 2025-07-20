import httpx
from typing import Any

class ExternalMessenger:
    """
    Пример интеграции с внешним API (отправка сообщения через httpx).
    """
    
    @staticmethod
    async def send_message(
        to: str,
        text: str,
        api_url: str,
        api_token: str | None = None
    ) -> dict[str, Any]:
        """
        Отправить сообщение через внешний API (например, Telegram, SMS, email).

        Args:
            to (str): Кому отправить (номер, email, chat_id и т.д.).
            text (str): Текст сообщения.
            api_url (str): URL внешнего API.
            api_token (str | None): Токен для авторизации (если требуется).

        Returns:
            dict[str, Any]: Ответ от внешнего API (или мок).
        """
        headers = {}
        if api_token:
            headers["Authorization"] = f"Bearer {api_token}"
            
        payload = {
            "to": to,
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    api_url,
                    json=payload,
                    headers=headers
                    )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                status_code = getattr(getattr(e, "response", None), "status_code", None)
                return {
                    "error": str(e),
                    "status_code": status_code
                }