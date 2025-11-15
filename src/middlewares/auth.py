from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.db.models import User
from src.lexicon.lexicon_ru import LEXICON_RU

class AuthMiddleware(BaseMiddleware):
    """
    Middleware для проверки, зарегистрирован ли пользователь в базе данных.
    """
    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        user = data.get('event_from_user')

        # Проверяем наличие пользователя в базе данных
        async with self.session_pool() as session:
            is_registered = await session.get(User, user.id)
        
        # Если пользователь зарегистрирован, пропускаем дальше
        if is_registered:
            return await handler(event, data)
        
        # Если не зарегистрирован, отвечаем и прерываем обработку
        if isinstance(event, Message):
            await event.answer(LEXICON_RU.AUTH_REQUIRED)
        elif isinstance(event, CallbackQuery):
            await event.answer(LEXICON_RU.AUTH_REQUIRED, show_alert=True)
        return
