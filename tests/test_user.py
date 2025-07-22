import asyncio

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.app.api.user import router as user_router
from src.app.core.config import settings
from src.app.core.database import get_db
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

    TEST_DATABASE_URL = settings.TEST_DATABASE_URL
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async def recreate_tables():
        async with engine.begin() as conn:
            await conn.run_sync(UserBase.metadata.drop_all)
            await conn.run_sync(UserBase.metadata.create_all)

    @pytest.fixture(autouse=True)
    async def _reset_db():
        await recreate_tables()

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    return app, recreate_tables


@pytest.mark.asyncio
async def test_register_login_update_delete_user(test_app):
    app, recreate_tables = await test_app
    await recreate_tables()  # Сбросить БД перед тестом

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Регистрация юзера
        user_data = {
            "username": "testuser",
            "password": "Test123321@",
            "email": "testuser@ex.com",
            "full_name": "Nick Kcin",
        }
        response = await ac.post("/users/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        user = response.json()
        user_id = user["id"]

        # Логин
        login_data = {"email": "testuser@ex.com", "password": "Test123321@"}
        response = await ac.post("/users/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        access_token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Получить пользователя по id
        response = await ac.get(f"/users/{user_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        user_info = response.json()
        assert user_info["email"] == "testuser@ex.com"

        # Обновление данных
        update_data = {"full_name": "Kick Nick"}
        response = await ac.patch(
            f"/users/{user_id}", json=update_data, headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        updated = response.json()
        assert updated["full_name"] == "Kick Nick"

        # Удаление пользователя
        response = await ac.delete(f"/users/{user_id}", headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
