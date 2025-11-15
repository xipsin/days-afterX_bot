import os
import sys
from dotenv import load_dotenv

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# ----------------- НАЧАЛО НАШИХ ИЗМЕНЕНИЙ -----------------

# Добавляем корень проекта в пути Python
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

# Импортируем нашу базовую модель
from src.db.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Переопределяем URL для подключения к БД из переменной окружения
# Это самая важная строка, которая решает нашу проблему
if os.environ.get('DATABASE_URL'):
    config.set_main_option('sqlalchemy.url', os.environ['DATABASE_URL'])
else:
    # На случай если переменная не установлена, оставляем фолбэк на alembic.ini
    # Но в нашем Docker-сетапе она всегда будет установлена
    pass

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем Alembic на метаданные наших моделей
target_metadata = Base.metadata

# ----------------- КОНЕЦ НАШИХ ИЗМЕНЕНИЙ -------------------


# ... остальной сгенерированный код оставляем без изменений ...


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

