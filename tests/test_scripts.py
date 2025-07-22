import asyncio

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

from src.app.api.script import router as script_router
from src.app.api.user import router as user_router
from src.app.core.config import settings
from src.app.core.database import get_db
from src.app.models.script import Base as ScriptBase
from src.app.models.user import Base as UserBase


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_app():
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(script_router)

    TEST_DATABASE_URL = settings.TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def recreate_tables():
        async with engine.begin() as conn:
            await conn.run_sync(UserBase.metadata.drop_all)
            await conn.run_sync(ScriptBase.metadata.drop_all)
            await conn.run_sync(UserBase.metadata.create_all)
            await conn.run_sync(ScriptBase.metadata.create_all)

    await recreate_tables()

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.mark.asyncio
async def test_create_update_delete_script(test_app):
    app = await test_app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Регистрация пользователя
        user_data = {
            "username": "testuser",
            "password": "Test123321@",
            "email": "testuser@ex.com",
            "full_name": "Nick Kcin",
        }
        await ac.post("/users/register", json=user_data)

        # Логин
        login_data = {
            "email": "testuser@ex.com",
            "password": "Test123321@"
            }
        response = await ac.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        access_token = response.json()["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}"
            }
        # Создание скрипта
        script_data = {
            "name": "Test script",
            "content": "Hi {{name}}!"
            }
        response = await ac.post(
            "/scripts/",
            json=script_data,
            headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        script = response.json()
        script_id = script["id"]
        assert script["name"] == "Test script"
        assert script["content"] == "Hi {{name}}!"

        # Обновление скрипта
        update_data = {"name": "Update script", "content": "Updated content"}
        response = await ac.patch(
            f"/scripts/{script_id}", json=update_data, headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        updated = response.json()
        assert updated["name"] == "Update script"
        assert updated["content"] == "Updated content"

        # Удаление скрипта
        response = await ac.delete(f"/scripts/{script_id}", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
