from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.config import logger, DATABASE_URL

# Проверяем, что URL для подключения к БД загружен
if not DATABASE_URL:
    logger.critical("Не удалось загрузить DATABASE_URL! Проверьте .env файл.")
    exit("Database URL not found!")

try:
    # Создаем асинхронный "движок" для подключения к БД
    # echo=False, чтобы не выводить в лог все SQL-запросы. В режиме DEBUG можно поставить True.
    engine = create_async_engine(DATABASE_URL, echo=False)

    # Создаем фабрику асинхронных сессий
    # expire_on_commit=False, чтобы объекты были доступны после коммита
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

except Exception as e:
    logger.critical(f"Не удалось подключиться к базе данных: {e}")
    exit(f"Database connection failed: {e}")

# Базовый класс для всех наших будущих моделей (таблиц)
Base = declarative_base()

logger.info("Подключение к базе данных настроено успешно.")

