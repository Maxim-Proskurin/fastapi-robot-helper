import uvicorn
from fastapi import FastAPI
from src.app.api.user import router as user_router
from src.app.api.script import router as script_router
from src.app.api.integration import router as integration_router
from src.app.api.regexp import router as regexp_router
from src.app.utils.utils import custom_openapi


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Robot Helper",
        description=(
            "API для управления пользователями,"
            "скриптами, интеграциями и regexp."),
        version="1.0.0")
    app.include_router(user_router)
    app.include_router(script_router)
    app.include_router(integration_router)
    app.include_router(regexp_router)

    app.openapi = custom_openapi.__get__(app)

    @app.get("/", tags=["health"])
    async def root():
        return {"status": "ok", "message": "FastAPI Robot Helper is running!"}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
