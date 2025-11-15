# Этап 1: Сборка зависимостей
FROM python:3.11-slim as builder

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта, которые определяют зависимости
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости без dev-пакетов и в отдельную папку
RUN poetry install --no-dev --no-interaction --no-ansi

# Этап 2: Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные зависимости
COPY --from=builder /usr/local/lib/python3.11/site-packages ./

# Копируем исходный код
COPY src/ ./src/

CMD ["python", "src/main.py"]
