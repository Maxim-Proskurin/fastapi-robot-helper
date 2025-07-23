FROM python:3.12

WORKDIR /app

# Сначала копируем исходный код и README.md
COPY src/ /app/src/
COPY README.md /app/
COPY pyproject.toml poetry.lock* /app/

# Затем устанавливаем poetry и зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Миграции и конфиги
COPY alembic/ /app/alembic/
COPY alembic.ini /app/
COPY .env /app/

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
