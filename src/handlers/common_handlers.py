from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.db.database import async_session_maker
from src.db.models import User
from src.config import logger
from src.lexicon.lexicon_ru import LEXICON_RU

# Создаем роутер для общих, публичных команд
router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    user = message.from_user
    logger.info(f"Пользователь {user.id} ({user.full_name}) вызвал /start")
    try:
        async with async_session_maker() as session:
            if not await session.get(User, user.id):
                new_user = User(id=user.id, username=user.username, full_name=user.full_name)
                session.add(new_user)
                await session.commit()
                logger.info(f"Новый пользователь {user.id} успешно зарегистрирован.")
                response = LEXICON_RU.GREETING_NEW_USER.format(full_name=user.full_name)
            else:
                logger.info(f"Пользователь {user.id} уже существует.")
                response = LEXICON_RU.GREETING_EXISTING_USER.format(full_name=user.full_name)
            await message.answer(response)
    except Exception as e:
        logger.error(f"Ошибка при обработке /start для {user.id}: {e}")
        await message.answer(LEXICON_RU.REGISTRATION_ERROR)
