# Этап 1: Сборка зависимостей
FROM python:3.11-slim as builder

# Устанавливаем Poetry - наш менеджер зависимостей
RUN pip install poetry

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы, определяющие зависимости проекта
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости с помощью Poetry.
# --no-root: не устанавливать сам проект как пакет, только его зависимости.
# --without dev: исключить пакеты для разработки (например, pytest).
# --no-interaction, --no-ansi: флаги для работы в автоматизированных средах (CI/CD).
# --sync: гарантирует, что окружение точно соответствует lock-файлу.
RUN poetry install --no-root --without dev --no-interaction --no-ansi --sync

# Этап 2: Финальный, легковесный образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем установленные на предыдущем этапе зависимости.
# Используем wildcard (*), так как Poetry создает папку с уникальным хэшем.
COPY --from=builder /root/.cache/pypoetry/virtualenvs/days-after-x-bot-*/lib/python3.11/site-packages ./

# Копируем исходный код нашего приложения
COPY src/ ./src/

# Команда для запуска приложения.
# Используем флаг -m, чтобы запустить 'src.main' как модуль.
# Это позволяет Python корректно обрабатывать внутренние импорты (например, from src.config).
CMD ["python", "-m", "src.main"]
