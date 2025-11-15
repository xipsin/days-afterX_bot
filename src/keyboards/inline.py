from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.lexicon.lexicon_ru import LEXICON_RU

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру с одной кнопкой 'Отмена'.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU.KEYBOARDS['cancel'], callback_data="fsm_cancel")
    )
    return builder.as_markup()


def get_date_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для выбора даты, включая кнопку отмены.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU.KEYBOARDS['today'], callback_data="date_select:today"),
        InlineKeyboardButton(text=LEXICON_RU.KEYBOARDS['yesterday'], callback_data="date_select:yesterday")
    )
    builder.row(
        InlineKeyboardButton(text=LEXICON_RU.KEYBOARDS['cancel'], callback_data="fsm_cancel")
    )
    return builder.as_markup()
