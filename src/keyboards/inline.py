from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon.lexicon_ru import LEXICON_RU

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с кнопкой 'Отмена' для FSM-диалогов.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['cancel'],
            callback_data="fsm_cancel"
        )
    )
    return builder.as_markup()

def get_date_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для выбора даты ('Сегодня', 'Вчера') и отмены.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['today'],
            callback_data="date_select:today"
        ),
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['yesterday'],
            callback_data="date_select:yesterday"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['cancel'],
            callback_data="fsm_cancel"
        )
    )
    return builder.as_markup()

def get_list_actions_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с действиями для списка событий,
    расположенными вертикально.
    """
    builder = InlineKeyboardBuilder()
    # Каждая кнопка в новой строке
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['add_event'], 
            callback_data="add_event"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['reset_event'], 
            callback_data="reset_event"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.KEYBOARDS['delete_event'], 
            callback_data="delete_event"
        )
    )
    return builder.as_markup()
