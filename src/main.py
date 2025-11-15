import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties # Импортируем

from src.config import logger, TELEGRAM_BOT_TOKEN
from src.handlers import user_handlers

async def main():
    logger.info("Бот запускается...")

    # Создаем объект с настройками по умолчанию
    default_properties = DefaultBotProperties(parse_mode="HTML")

    # Инициализация Bot с новым синтаксисом
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
