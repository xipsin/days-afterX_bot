import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Переменные окружения ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- Настройки бизнес-логики ---
# Максимальный возраст события в годах, которое можно добавить.
MAX_EVENT_AGE_YEARS = int(os.getenv("MAX_EVENT_AGE_YEARS", 100))


# --- Настройка логирования ---
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Проверка, что ключевые переменные загружены
if not TELEGRAM_BOT_TOKEN:
    logger.critical("Не удалось загрузить токен Telegram-бота! Проверьте .env файл.")
    exit("Telegram bot token not found!")

if not DATABASE_URL:
    logger.critical("Не удалось загрузить DATABASE_URL! Проверьте .env файл.")
    exit("Database URL not found!")
