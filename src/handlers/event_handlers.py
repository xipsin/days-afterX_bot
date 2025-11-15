from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, User as TgUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.db.database import async_session_maker
from src.db.models import Event
from src.config import logger, MAX_EVENT_AGE_YEARS
from src.utils.text_parser import parse_add_command
from src.utils.formatters import format_days_passed
from src.handlers.states import AddEvent
from src.keyboards.inline import get_date_selection_keyboard, get_cancel_keyboard, get_list_actions_keyboard
from src.lexicon.lexicon_ru import LEXICON_RU
from src.middlewares.auth import AuthMiddleware

# Роутер для команд, связанных с событиями.
router = Router()

# Применяем AuthMiddleware к этому роутеру
router.message.middleware(AuthMiddleware(session_pool=async_session_maker))
router.callback_query.middleware(AuthMiddleware(session_pool=async_session_maker))


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (без декораторов) ---

async def _create_event(session: AsyncSession, user_id: int, name: str, date: datetime.date) -> Event:
    """Создает и сохраняет новое событие."""
    new_event = Event(user_id=user_id, name=name, event_date=date)
    session.add(new_event)
    await session.commit()
    logger.info(f"Пользователь {user_id} добавил событие: '{name}'")
    return new_event

async def _process_quick_add(message: Message, session: AsyncSession):
    """Обрабатывает сценарий быстрого добавления."""
    event_name, parsed_date = parse_add_command(message.text.replace("/add", "").strip())
    if not event_name:
        await message.answer(LEXICON_RU.ADD_ERROR_NO_NAME_QUICK)
        return
    event_date = parsed_date or message.date
    await _validate_and_create_event(message, message.from_user, session, event_name, event_date)

async def _validate_and_create_event(message: Message, user: TgUser, session: AsyncSession, name: str, date: datetime, state: FSMContext = None):
    """Общая функция для валидации даты и создания события."""
    user_now = message.date
    today_date = user_now.date()
    check_date = date.date()

    if check_date > today_date:
        await message.answer(LEXICON_RU.ADD_ERROR_FUTURE_DATE)
        if state: await state.clear()
        return
    
    max_age_delta = timedelta(days=365 * MAX_EVENT_AGE_YEARS)
    if check_date < (today_date - max_age_delta):
        await message.answer(LEXICON_RU.ADD_ERROR_TOO_OLD.format(max_years=MAX_EVENT_AGE_YEARS))
        if state: await state.clear()
        return

    try:
        await _create_event(session, user.id, name, check_date)
        await message.answer(LEXICON_RU.ADD_SUCCESS.format(event_name=name, event_date=check_date.strftime('%d.%m.%Y')))
    except Exception as e:
        logger.error(f"Ошибка при создании события для {user.id}: {e}")
        await message.answer(LEXICON_RU.ADD_ERROR_GENERAL)
    finally:
        if state:
            await state.clear()


# --- ХЭНДЛЕРЫ ДЛЯ ЭТОГО РОУТЕРА ---

@router.message(Command("add"))
async def process_add_command(message: Message, state: FSMContext, session: AsyncSession):
    """Точка входа для команды /add."""
    command_text = message.text.replace("/add", "").strip()
    if command_text:
        await _process_quick_add(message, session)
    else:
        await state.set_state(AddEvent.waiting_for_name)
        await message.answer(
            LEXICON_RU.ADD_PROMPT_NAME,
            reply_markup=get_cancel_keyboard()
        )

@router.message(Command("list"))
async def process_list_command(message: Message, session: AsyncSession):
    """Выводит нумерованный список всех событий пользователя с кнопками действий."""
    logger.info(f"Пользователь {message.from_user.id} вызвал /list")
    
    user_events = await session.execute(
        select(Event).where(Event.user_id == message.from_user.id).order_by(Event.created_at)
    )
    events = user_events.scalars().all()
    
    if not events:
        await message.answer(
            LEXICON_RU.LIST_EMPTY,
            reply_markup=get_list_actions_keyboard()
        )
        return
        
    response_lines = [LEXICON_RU.LIST_HEADER]
    today = datetime.now().date()
    
    for i, event in enumerate(events, 1):
        days_passed = (today - event.event_date).days
        days_passed_str = format_days_passed(days_passed)
        
        response_lines.append(
            LEXICON_RU.LIST_ITEM.format(
                number=i,
                event_name=event.name,
                days_passed_str=days_passed_str
            )
        )
        
    await message.answer(
        "\n".join(response_lines), 
        reply_markup=get_list_actions_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "add_event")
async def process_add_event_press(callback: CallbackQuery, state: FSMContext):
    """Реагирует на кнопку 'Добавить новое', запуская FSM для /add."""
    await callback.message.delete()
    await state.set_state(AddEvent.waiting_for_name)
    await callback.message.answer(
        LEXICON_RU.ADD_PROMPT_NAME,
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "reset_event")
async def process_reset_event_press(callback: CallbackQuery):
    """Заглушка для кнопки 'Сбросить счетчик'."""
    await callback.answer(
        text=LEXICON_RU.RESET_IN_DEVELOPMENT, 
        show_alert=True
    )

@router.callback_query(F.data == "delete_event")
async def process_delete_event_press(callback: CallbackQuery):
    """Заглушка для кнопки 'Удалить событие'."""
    await callback.answer(
        text=LEXICON_RU.DELETE_IN_DEVELOPMENT, 
        show_alert=True
    )

@router.callback_query(F.data == "fsm_cancel")
async def process_fsm_cancel(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает отмену любого FSM-диалога."""
    await state.clear()
    await callback.message.edit_text(LEXICON_RU.ADD_CANCELLED)
    await callback.answer()

@router.message(AddEvent.waiting_for_name)
async def process_event_name_fsm(message: Message, state: FSMContext):
    """Шаг FSM: получает имя события."""
    await state.update_data(event_name=message.text)
    await state.set_state(AddEvent.waiting_for_date)
    await message.answer(LEXICON_RU.ADD_PROMPT_DATE, reply_markup=get_date_selection_keyboard())

@router.callback_query(F.data.startswith("date_select:"))
async def process_date_button_fsm(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Шаг FSM: обрабатывает нажатие кнопок 'Сегодня'/'Вчера'."""
    selection = callback.data.split(":")[1]
    event_date = callback.message.date
    if selection == "yesterday":
        event_date -= timedelta(days=1)
    user_data = await state.get_data()
    event_name = user_data.get("event_name")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await _validate_and_create_event(callback.message, callback.from_user, session, event_name, event_date, state)

@router.message(AddEvent.waiting_for_date)
async def process_date_text_fsm(message: Message, state: FSMContext, session: AsyncSession):
    """Шаг FSM: обрабатывает ручной ввод даты."""
    _, parsed_date = parse_add_command(message.text)
    if not parsed_date:
        await message.answer(
            LEXICON_RU.ADD_ERROR_INVALID_DATE,
            reply_markup=get_date_selection_keyboard()
        )
        return
    user_data = await state.get_data()
    event_name = user_data.get("event_name")
    await _validate_and_create_event(message, message.from_user, session, event_name, parsed_date, state)
