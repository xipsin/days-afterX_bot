import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.config import logger, TELEGRAM_BOT_TOKEN
from src.handlers import user_handlers
from src.db.database import engine # <-- Импортируем наш движок

async def main():
    logger.info("Бот запускается...")

    # Проверка подключения к базе данных
    try:
        async with engine.connect() as conn:
            logger.info("Успешное подключение к базе данных!")
    except Exception as e:
        logger.critical(f"Ошибка подключения к базе данных: {e}")
        return # Завершаем работу, если не можем подключиться к БД

    default_properties = DefaultBotProperties(parse_mode="HTML")
    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=default_properties)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    logger.info("Хэндлеры подключены.")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Запуск polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен.")

