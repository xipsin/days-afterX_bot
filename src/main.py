import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import logger, TELEGRAM_BOT_TOKEN, DATABASE_URL
from src.db.database import async_session_maker
from src.handlers import common_handlers, event_handlers


async def main():
    """Основная функция для запуска бота."""

    # Настройка и проверка подключения к БД
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            logger.info("Успешное подключение к базе данных!")
    except Exception as e:
        logger.critical(f"Не удалось подключиться к базе данных: {e}")
        sys.exit("Database connection failed")

    # Инициализация бота и диспетчера
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="Markdown")
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)


    # Подключение роутеров
    dp.include_router(common_handlers.router)
    dp.include_router(event_handlers.router)
    logger.info("Все хэндлеры подключены.")

    # Запуск polling
    logger.info("Запуск polling...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")

