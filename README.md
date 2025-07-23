# FastAPI Robot Helper

Асинхронный сервис-робот на FastAPI для автоматизации и интеграции.
**REST API, JWT-аутентификация, PostgreSQL, Docker, CI/CD.**

[![build](https://github.com/Maxim-Proskurin/fastapi-robot-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/Maxim-Proskurin/fastapi-robot-helper/actions)
[![codecov](https://codecov.io/gh/Maxim-Proskurin/fastapi-robot-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/Maxim-Proskurin/fastapi-robot-helper)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Maxim-Proskurin/fastapi-robot-helper/main.svg)](https://results.pre-commit.ci/latest/github/Maxim-Proskurin/fastapi-robot-helper/main)

## ⚡️ Быстрый старт

```bash
git clone https://github.com/Maxim-Proskurin/fastapi-robot-helper.git
cd fastapi-robot-helper

cp .env.example .env
docker-compose up --build
```

- Документация API: http://localhost:8000/docs

## 💡 Технологии и стек

- **Python 3.12+**
- **FastAPI** — REST API backend
- **SQLAlchemy [async]** — ORM, асинхронный доступ к БД
- **PostgreSQL 15**
- **Alembic** — миграции схемы БД
- **Pydantic v2**
- **python-jose** — JWT
- **passlib[bcrypt]**
- **httpx**
- **pytest, pytest-asyncio, pytest-cov**
- **isort, black, flake8, mypy**
- **Poetry** — управление зависимостями
- **Docker, Docker Compose**
- **GitHub Actions**
- **python-dotenv**

## 🏗️ Архитектура

- Асинхронный FastAPI backend
- JWT (access/refresh)
- PostgreSQL через async SQLAlchemy
- Миграции через Alembic
- CI/CD: тесты, линтеры, покрытие, миграции
- Контейнеризация через Docker Compose

## 🚀 Запуск без Docker (локально)

```bash
pip install poetry
poetry install
poetry shell

# Настройте .env (см. .env.example)
alembic upgrade head
uvicorn src.main:app --reload
```

## 🧪 Тестирование и покрытие

```bash
poetry run pytest --cov=src
poetry run pytest --cov=src --cov-report=html
# Откройте файл htmlcov/index.html в браузере
```
- [Онлайн-отчёт о покрытии тестов (Codecov)](https://codecov.io/gh/Maxim-Proskurin/fastapi-robot-helper)
  _(или откройте `htmlcov/index.html` после локального теста)_

## 🗂️ Структура проекта

```
.
├── src/
│   ├── api/
│   ├── db/
│   ├── core/
│   └── main.py
├── tests/
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## 🛠️ Примеры API

- [Swagger/OpenAPI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

## 📦 Переменные окружения

Настройки через `.env` (см. `.env.example`).

## 👨‍💻 CI/CD

- **GitHub Actions:** автотесты, линтеры, покрытие, миграции.
- **pre-commit:** автоформатирование и проверка кода ([интеграция с pre-commit.ci](https://pre-commit.ci/)).

## 📋 Лицензия

MIT

---

_Для вопросов и предложений: [Issues](https://github.com/Maxim-Proskurin/fastapi-robot-helper/issues)_
