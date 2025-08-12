# FastAPI Robot Helper

Асинхронный сервис-робот на FastAPI для автоматизации и интеграции.
**REST API, JWT-аутентификация, PostgreSQL, Docker, CI/CD.**

[![build](https://github.com/Maxim-Proskurin/fastapi-robot-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/Maxim-Proskurin/fastapi-robot-helper/actions)
[![codecov](https://codecov.io/gh/Maxim-Proskurin/fastapi-robot-helper/branch/main/graph/badge.svg)](https://codecov.io/gh/Maxim-Proskurin/fastapi-robot-helper)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://pycqa.github.io/isort/)
[![flake8](https://img.shields.io/badge/lint-flake8-blue.svg)](https://flake8.pycqa.org/en/latest/)

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

```

## 🗂️ Структура проекта

```text
.
├── src/
│   └── app/
│       ├── api/           # Роутеры FastAPI (user, script, integration, regexp)
│       ├── core/          # Конфиг, база, JWT, зависимости
│       ├── models/        # SQLAlchemy модели
│       ├── schemas/       # Pydantic схемы
│       ├── service/       # Бизнес-логика (user, script, integration, regexp)
│       ├── utils/         # Вспомогательные функции
│       ├── depends/       # Зависимости FastAPI (auth и др.)
│       └── main.py        # Точка входа FastAPI
├── tests/                 # Pytest тесты
├── alembic/               # Миграции Alembic
│   ├── versions/          # Файлы миграций
│   └── env.py             # Alembic конфиг
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
