from aiogram import types
from aiogram.filters import Filter


class IsPrivate(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type == 'private'
