from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from src.db.database import async_session_maker
from src.db.models import User
from src.config import logger

# Создаем новый роутер для пользовательских команд
router = Router()

# Этот хэндлер будет срабатывать на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Обработчик команды /start.
    Приветствует пользователя и регистрирует его в базе данных, если он новый.
    """
    user = message.from_user
    user_name = user.full_name
    logger.info(f"Пользователь {user.id} ({user_name}) вызвал /start")

    # Сохраняем пользователя в базу данных
    async with async_session_maker() as session:
        new_user = User(
            id=user.id,
            username=user.username,

            full_name=user.full_name
        )
        session.add(new_user)
        try:
            await session.commit()
            logger.info(f"Новый пользователь {user.id} успешно зарегистрирован.")
            await message.answer(
                f"Привет, **{user_name}**!\n\n"
                f"Рад знакомству. Я помогу тебе отслеживать дни после важных событий.\n\n"
                f"Используй команду /add, чтобы добавить новое событие."
            )
        except IntegrityError:
            await session.rollback()
            logger.info(f"Пользователь {user.id} уже существует в базе данных.")
            await message.answer(
                f"С возвращением, **{user_name}**!\n\n"
                f"Рад снова тебя видеть. Чтобы посмотреть список своих событий, используй команду /list."
            )
        except Exception as e:
            await session.rollback()
            logger.error(f"Произошла ошибка при регистрации пользователя {user.id}: {e}")
            await message.answer("Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.")

