from aiogram import Bot, Router
from aiogram.types import ChatJoinRequest
from sqlalchemy.ext.asyncio import AsyncSession

from crud.subscriber import subscribtion_crud


router = Router()


ACCESS_DENIED = (
    'Ошибка доступа. Активируйте ссылку-приглашение на аккаунте, '
    'с которого была произведена оплата'
)
WELCOME_MESSAGE = 'Добро пожаловать, {name}!'


@router.chat_join_request()
async def aproove_request(
    chat_join_request: ChatJoinRequest,
    session: AsyncSession,
    bot: Bot
):
    if subscribtion := await subscribtion_crud.get(
        session=session,
        id=chat_join_request.from_user.id
    ):
        await chat_join_request.approve()
        await bot.send_message(
            chat_id=chat_join_request.chat.id,
            text=WELCOME_MESSAGE.format(name=subscribtion.name)
        )
    else:
        await bot.send_message(
            chat_id=chat_join_request.from_user.id,
            text=ACCESS_DENIED
        )
