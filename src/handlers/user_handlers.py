from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

# Создаем новый роутер для пользовательских команд
router = Router()

# Этот хэндлер будет срабатывать на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Обработчик команды /start. Приветствует пользователя.
    """
    user_name = message.from_user.full_name
    await message.answer(
        f"Привет, {user_name}!\n\n"
        "Я — бот, который поможет тебе отслеживать дни после важных событий.\n\n"
        "Используй команду /add, чтобы добавить новое событие."
    )

