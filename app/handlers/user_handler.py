from datetime import datetime, timedelta


from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.types import ChatJoinRequest, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from crud.subscriber import subscription_crud


router = Router()

PRICE = types.LabeledPrice(label='Подписка хз на что', amount=50000)
EXPIRE_DATE = datetime.now() + timedelta(hours=1)


@router.message(Command(commands=['buy']))
async def process_buy_command(message: Message):
    await message.answer(text='Готовь баблишко')
    await message.answer_invoice(
        title='Заголовок',
        description='Описание',
        provider_token=settings.payment_token,
        currency='rub',
        prices=[PRICE],
        start_parameter='subscribe',
        payload='some_invoice_payload'
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: types.PreCheckoutQuery
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(
    message: Message,
    session: AsyncSession,
    bot: Bot
):
    subscription = await subscription_crud.create(
        session=session,
        id=message.from_user.id,
        name=message.from_user.first_name,
        subscribtion_period=1
    )
    await message.answer(
        f'Оплата прошла успешно \n'
        f'Подписка действительна до {subscription.end_date.strftime('%Y-%m-%d')}'
    )
    link = await bot.create_chat_invite_link(
        chat_id=-1002143176488,
        creates_join_request=True,
        expire_date=EXPIRE_DATE
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Ваша ссылка для вступления в группу:\n{link.invite_link}'
    )
