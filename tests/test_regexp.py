import asyncio

import pytest
from fastapi import FastAPI, status
from httpx import ASGITransport, AsyncClient
from src.app.api.regexp import router as regexp_router


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_app():
    app = FastAPI()
    app.include_router(regexp_router)
    return app


@pytest.mark.asyncio
async def test_extract_emails(test_app):
    app = await test_app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        data = {"text": "Contact: test@example.com, foo@bar.com"}
        response = await ac.post("/regexp/extract_emails", json=data)
        assert response.status_code == status.HTTP_200_OK
        emails = response.json().get("emails")
        assert "test@example.com" in emails
        assert "foo@bar.com" in emails


@pytest.mark.asyncio
async def test_extract_variables(test_app):
    app = await test_app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        data = {"text": "Hello, {{name}}! Your code: {{code}}"}
        response = await ac.post("/regexp/extract_variables", json=data)
        assert response.status_code == status.HTTP_200_OK
        variables = response.json().get("variables")
        assert "name" in variables
        assert "code" in variables


@pytest.mark.asyncio
async def test_validate_pattern(test_app):
    app = await test_app
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        data = {"pattern": r"\d{3}-\d{2}-\d{4}", "text": "123-45-6789"}
        response = await ac.post("/regexp/validate_pattern", json=data)
        assert response.status_code == status.HTTP_200_OK
        result = response.json().get("is_valid")
        assert result is True
