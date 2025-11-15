import asyncio
from src.config import logger, TELEGRAM_BOT_TOKEN

async def main():
    """
    Главная асинхронная функция для запуска бота.
    """
    logger.info("Бот запускается...")
    logger.debug(f"Токен: {TELEGRAM_BOT_TOKEN[:5]}...{TELEGRAM_BOT_TOKEN[-5:]}")

    # Здесь будет основная логика инициализации и запуска бота
    # Например, создание объектов Bot и Dispatcher из aiogram

    logger.info("Бот успешно запущен (симуляция).")
    # В будущем здесь будет бесконечный цикл работы бота
    # пока что просто завершаем работу для теста
    await asyncio.sleep(5) # немного подождем для наглядности
    logger.info("Бот завершает работу.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную.")

