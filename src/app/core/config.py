import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "")

    TEST_DB_NAME: str = os.getenv("TEST_DB_NAME", "")
    TEST_DB_URL: str = os.getenv("TEST_DB_URL", "")

    @property
    def DATABASE_URL(self) -> str:
        url = os.getenv("DATABASE_URL")
        return url if url is not None else ""

    @property
    def TEST_DATABASE_URL(self) -> str:
        url = os.getenv("TEST_DB_URL")
        if url and url.startswith("postgresql+psycopg2://"):
            url = url.replace(
                "postgresql+psycopg2://",
                "postgresql+asyncpg://"
                )
        return url if url is not None else ""


settings = Settings()
