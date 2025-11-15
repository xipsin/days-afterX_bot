from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

from src.db.database import async_session_maker
from src.db.models import User, Event
from src.config import logger, MAX_EVENT_AGE_YEARS
from src.utils.text_parser import parse_add_command

router = Router()

# --- Обработчик команды /start ---
@router.message(CommandStart())
async def process_start_command(message: Message):
    """
    Обработчик команды /start.
    Приветствует и регистрирует пользователя.
    """
    user = message.from_user
    logger.info(f"Пользователь {user.id} ({user.full_name}) вызвал /start")

    async with async_session_maker() as session:
        new_user = User(id=user.id, username=user.username, full_name=user.full_name)
        session.add(new_user)
        try:
            await session.commit()
            logger.info(f"Новый пользователь {user.id} успешно зарегистрирован.")
            await message.answer(
                f"Привет, **{user.full_name}**!\n\n"
                f"Рад знакомству. Я помогу тебе отслеживать дни после важных событий.\n\n"
                f"Используй команду `/add [Событие] [Дата]` для добавления нового события."
            )
        except IntegrityError:
            await session.rollback()
            logger.info(f"Пользователь {user.id} уже существует в базе данных.")
            await message.answer(
                f"С возвращением, **{user.full_name}**!\n\n"
                f"Чтобы посмотреть список своих событий, используй команду /list."
            )
        except Exception as e:
            await session.rollback()
            logger.error(f"Произошла ошибка при регистрации пользователя {user.id}: {e}")
            await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

# --- Обработчик команды /add ---
@router.message(Command("add"))
async def process_add_command(message: Message):
    """
    Обработчик команды /add.
    Добавляет новое событие для пользователя.
    """
    user = message.from_user
    user_now = message.date  # Используем время сообщения для коррекции часовых поясов
    command_text = message.text.replace("/add", "").strip()

    # 1. Валидация: команда не должна быть пустой
    if not command_text:
        await message.answer(
            "Пожалуйста, укажите название события.\n"
            "Например: `/add Поменял масло в машине 01.10.2025`\n"
            "Или просто: `/add Полить цветы` (будет установлена сегодняшняя дата)."
        )
        return

    # 2. Парсинг текста команды
    event_name, parsed_date = parse_add_command(command_text)

    # 3. Валидация: название события не должно быть пустым после парсинга
    if not event_name:
        await message.answer("Пожалуйста, укажите название события. Вы указали только дату.")
        return

    # 4. Определение и валидация даты
    event_date = parsed_date or user_now

    if event_date.date() > user_now.date():
        await message.answer("Ошибка: нельзя установить дату события в будущем.")
        return
    
    max_age_delta = timedelta(days=365 * MAX_EVENT_AGE_YEARS)
    if event_date.date() < (user_now.date() - max_age_delta):
        await message.answer(f"Ошибка: дата события не может быть старше {MAX_EVENT_AGE_YEARS} лет.")
        return

    # 5. Сохранение в базу данных
    async with async_session_maker() as session:
        new_event = Event(
            user_id=user.id,
            name=event_name,
            event_date=event_date.date()
        )
        session.add(new_event)
        try:
            await session.commit()
            logger.info(f"Пользователь {user.id} добавил новое событие: '{event_name}'")
            await message.answer(
                f"✅ Событие **'{event_name}'** успешно добавлено с датой **{event_date.strftime('%d.%m.%Y')}**."
            )
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении события для пользователя {user.id}: {e}")
            await message.answer("Не удалось добавить событие. Произошла ошибка.")
