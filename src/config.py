import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
# Ищем .env файл относительно базовой директории проекта
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Переменные окружения ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# --- Настройка логирования ---
# Устанавливаем базовую конфигурацию для логирования
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# Получаем корневой логгер
logger = logging.getLogger(__name__)

# Проверка, что токен бота загружен
if not TELEGRAM_BOT_TOKEN:
    logger.critical("Не удалось загрузить токен Telegram-бота! Проверьте .env файл.")
    exit("Telegram bot token not found!")

