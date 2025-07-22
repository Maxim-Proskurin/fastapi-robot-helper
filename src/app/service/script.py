import contextlib
import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.script import Script
from src.app.schemas.script import ScriptCreate, ScriptUpdate


class ScriptService:
    @staticmethod
    async def create_script(
        script_data: ScriptCreate, user_id: UUID, db: AsyncSession
    ) -> Script:
        """
        Создать новый скрипт для пользователя.

        Args:
            script_data (ScriptCreate): Данные для создания скрипта.
            user_id (UUID): Идентификатор пользователя-владельца.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            Script: Созданный скрипт.

        Raises:
            ValueError: Если скрипт не был создан (неожиданная ошибка).
        """
        script = Script(
            name=script_data.name, content=script_data.content, user_id=user_id
        )
        db.add(script)
        await db.commit()
        await db.refresh(script)
        if not script:
            raise ValueError("Скрипт не был создан")
        return script

    @staticmethod
    async def get_script(script_id: UUID, db: AsyncSession) -> Script | None:
        """
        Получить скрипт по его идентификатору.

        Args:
            script_id (UUID или str): Идентификатор скрипта.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            Script | None: Скрипт, если найден, иначе None.
        """
        if isinstance(script_id, str):
            with contextlib.suppress(Exception):
                script_id = uuid.UUID(script_id)

        result = await db.execute(select(Script).where(Script.id == script_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list_scripts(
        user_id: UUID,
        db: AsyncSession,
    ) -> list[Script]:
        """
        Получить все скрипты пользователя.

        Args:
            user_id (UUID): Идентификатор пользователя.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            list[Script]: Список скриптов пользователя.
        """
        result = await db.execute(
            select(Script)
            .where(Script.user_id == user_id)
            )
        return list(result.scalars().all())

    @staticmethod
    async def update_script(
        script_id, script_data: ScriptUpdate, db: AsyncSession
    ) -> Script | None:
        """
        Обновить скрипт по идентификатору.

        Args:
            script_id (UUID): Идентификатор скрипта.
            script_data (ScriptUpdate): Данные для обновления скрипта.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            Script | None: Обновлённый скрипт, если найден, иначе None.
        """
        if isinstance(script_id, str):
            with contextlib.suppress(Exception):
                script_id = uuid.UUID(script_id)

        result = await db.execute(select(Script).where(Script.id == script_id))
        script = result.scalar_one_or_none()
        if not script:
            return None
        update_data = script_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(script, field, value)
        await db.commit()
        await db.refresh(script)
        return script

    @staticmethod
    async def delete_script(script_id, db: AsyncSession) -> bool:
        """
        Удалить скрипт по идентификатору.

        Args:
            script_id (UUID): Идентификатор скрипта.
            db (AsyncSession): Асинхронная сессия БД.

        Returns:
            bool: True, если скрипт удалён, иначе False.
        """
        if isinstance(script_id, str):
            with contextlib.suppress(Exception):
                script_id = uuid.UUID(script_id)

        result = await db.execute(select(Script).where(Script.id == script_id))
        script = result.scalar_one_or_none()
        if not script:
            return False
        await db.delete(script)
        await db.commit()
        return True
