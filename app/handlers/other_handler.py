from aiogram import Bot, F, Router, types
from aiogram.types import ChatJoinRequest, Message
from sqlalchemy.ext.asyncio import AsyncSession


from crud.subscriber import subscription_crud

router = Router()


@router.chat_join_request()
async def aproove_request(
    chat_join_request: ChatJoinRequest,
    session: AsyncSession,
    bot: Bot
):
    if subscription := await subscription_crud.get(
        session=session,
        id=chat_join_request.from_user.id
    ):
        await chat_join_request.approve()
        await bot.send_message(
            chat_id=chat_join_request.chat.id,
            text=f'{subscription.name} вступил в группу'
        )
    else:
        await bot.send_message(
            chat_id=chat_join_request.from_user.id,
            text='Подписка на канал не была оплачена'
        )
