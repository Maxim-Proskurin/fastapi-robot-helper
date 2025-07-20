from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.script import (
    ScriptCreate,
    ScriptRead,
    ScriptUpdate
)
from src.app.service.script import ScriptService
from src.app.core.database import get_db
from src.app.api.user import get_current_user_id

from uuid import UUID

router = APIRouter(prefix="/scripts", tags=["scripts"])


@router.post(
    "/",
    response_model=ScriptRead,
    status_code=status.HTTP_201_CREATED
)
async def create_script(
    script_data: ScriptCreate,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """
    Создать новый скрипт для пользователя.

    Args:
        script_data (ScriptCreate): Данные для создания скрипта
        db (AsyncSession, optional):Асинхронная сессия БД.
    
    Returns:
        ScriptRead: Данные созданного скрипта.
    """
    script = await ScriptService.create_script(script_data, user_id, db)
    return script

@router.patch("/{script_id}", response_model=ScriptRead)
async def update_script(
    script_id: UUID,
    script_data: ScriptUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить скрипт по id.

    Args:
        script_id (UUID): Идентификатор скрипта.
        script_data (ScriptUpdate): Данные для обновления скрипта.
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        ScriptRead: Обновлённые данные скрипта.

    Raises:
        HTTPException: Если скрипт не найден.
    """
    script = await ScriptService.update_script(
        script_id,
        script_data,
        db
        )
    if not script:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Скрипт не найден"
        )
    return script

@router.delete(
    "/{script_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_script(
    script_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить скрипт по id.

    Args:
        script_id (UUID): Идентификатор скрипта.
        db (AsyncSession): Асинхронная сессия БД.

    Returns:
        None

    Raises:
        HTTPException: Если скрипт не найден.
    """
    deleted = await ScriptService.delete_script(script_id,db)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Скрипт не найден."
        )
    return None
    
