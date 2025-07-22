import asyncio

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.api.integration import router as integration_router
from src.app.api.user import router as user_router
from src.app.core.config import settings
from src.app.core.database import get_db
from src.app.models.user import Base as UserBase


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_app():
    app = FastAPI()
    app.include_router(user_router)
    app.include_router(integration_router)

    TEST_DATABASE_URL = settings.TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def recreate_tables():
        async with engine.begin() as conn:
            await conn.run_sync(UserBase.metadata.drop_all)
            await conn.run_sync(UserBase.metadata.create_all)

    await recreate_tables()

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return app, recreate_tables


@pytest.mark.asyncio
async def test_send_message_integration(test_app):
    app, recreate_tables = await test_app
    await recreate_tables()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Регистрация пользователя
        user_data = {
            "username": "integrationuser",
            "password": "Test123321@",
            "email": "integrationuser@ex.com",
            "full_name": "Integration User",
        }
        await ac.post("/users/register", json=user_data)

        # Логин
        login_data = {
            "email": "integrationuser@ex.com",
            "password": "Test123321@"
            }
        response = await ac.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Тест интеграции (пример запроса)
        message_data = {
            "to": "test@example.com",
            "text": "Hello from integration test!",
            "api_url": "https://example.com/api",
            "api_token": "fake-token",
        }
        response = await ac.post(
            "/integration/send_message",
            json=message_data,
            headers=headers
        )
        # Ожидаем либо 200, либо 502 (если внешний API не доступен)
        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_502_BAD_GATEWAY
            )
