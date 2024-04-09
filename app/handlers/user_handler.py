from datetime import datetime, timedelta


from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery, ContentType, LabeledPrice, Message, PreCheckoutQuery
)
from sqlalchemy.ext.asyncio import AsyncSession

from filters.filters import IsPrivate
from core.config import settings
from crud.subscriber import subscribtion_crud
from keyboards.keyboards import (
    choose_action_keyboard, invoice_keyboard, tariffs_keyboard,
    BACK_BUTTON_CALLBACK, TARIFFS_LIST_BUTTON_TEXT,
    MY_SUBSCRIBTION_BUTTON_TEXT, ONE_MONTH_BUTTON_CALLBACK,
    ONE_MONTH_BUTTON_TEXT, TWO_MONTH_BUTTON_TEXT, TWO_MONTH_BUTTON_CALLBACK
)


router = Router()

LINK_EXPIRE_TIME = datetime.now() + timedelta(hours=1)
FORMAT = '%Y-%m-%d'

INVOICE_PRICE_AMOUNT = 50000

CHOOSE_TARIFF = 'Выберете срок действия подписки'
INVITE = (
    'Ваша ссылка для вступления в группу:\n'
    '{link}'
)
INVOICE_LABLE = 'Подписка на тестовую группу'
INVOICE_DESCRIPTION = 'Выберете способ оплаты'
INVOICE_CURRENCY = 'rub'
INVOICE_START_PARAMETER = 'subscribe'
SUBSCRIBTION_CREATE = (
    'Оплата прошла успешно \n'
    'Подписка действительна до {end_date}'
)
SUBSCRIBTION_UPDATE = (
    'Вы успешно продлили срок действия подписки \n'
    'Новая подписка действительна до {end_date}'
)
SUBSCRIBTION_WAS_FOUND = 'Подписка действительна до {end_date}.'
SUBSCRIBTION_WAS_NOT_FOUND = 'Действующих подписок не найдено.'
START_MESSAGE = (
    'Бот для оплаты подписок работает в тестовом режиме.\n\n'
    'Для совершения платежа используйте следующие реквизиты:\n\n'
    '1111 1111 1111 1026\n'
    '12/22, CVC 000'
)


@router.message(F.text == TARIFFS_LIST_BUTTON_TEXT, IsPrivate())
async def process_choose_tarrifs(message: Message):
    await message.answer(
        text=CHOOSE_TARIFF,
        reply_markup=tariffs_keyboard
    )


@router.message(F.text == MY_SUBSCRIBTION_BUTTON_TEXT, IsPrivate())
async def process_check_subcribtion(
    message: Message,
    session: AsyncSession,
):
    if subscribtion := await subscribtion_crud.get(
        session=session,
        id=message.from_user.id
    ):
        await message.answer(
            SUBSCRIBTION_WAS_FOUND.format(
                end_date=subscribtion.end_date.strftime(FORMAT)
            )
        )
    else:
        await message.answer(SUBSCRIBTION_WAS_NOT_FOUND)


@router.callback_query(F.data == BACK_BUTTON_CALLBACK)
async def process_back_command(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.delete()
    await process_choose_tarrifs(callback.message)


@router.callback_query(F.data.in_(
        {ONE_MONTH_BUTTON_CALLBACK, TWO_MONTH_BUTTON_CALLBACK})
)
async def process_buy_command(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    title = (
        ONE_MONTH_BUTTON_TEXT + ' подписки'
        if callback.data == ONE_MONTH_BUTTON_CALLBACK
        else TWO_MONTH_BUTTON_TEXT + ' подписки'
    )
    subscribtion_period = (
        int(ONE_MONTH_BUTTON_CALLBACK)
        if callback.data == ONE_MONTH_BUTTON_CALLBACK
        else int(TWO_MONTH_BUTTON_CALLBACK)
    )
    price = LabeledPrice(
        label=INVOICE_LABLE,
        amount=INVOICE_PRICE_AMOUNT * subscribtion_period
    )
    await callback.message.answer_invoice(
        title=title,
        description=INVOICE_DESCRIPTION,
        provider_token=settings.payment_token,
        currency=INVOICE_CURRENCY,
        prices=[price],
        start_parameter=INVOICE_START_PARAMETER,
        payload=str(subscribtion_period),
        reply_markup=invoice_keyboard
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(
    message: Message,
    session: AsyncSession,
    bot: Bot
):
    subscribtion_period = int(message.successful_payment.invoice_payload)
    if subscribtion := await subscribtion_crud.get(
        session=session,
        id=message.from_user.id
    ):
        subscribtion = await subscribtion_crud.update(
            session=session,
            subscribtion=subscribtion,
            subscribtion_period=subscribtion_period
        )
        await message.answer(
            SUBSCRIBTION_UPDATE.format(
                end_date=subscribtion.end_date.strftime(FORMAT)
            )
        )
    else:
        subscribtion = await subscribtion_crud.create(
            session=session,
            id=message.from_user.id,
            name=message.from_user.first_name,
            subscribtion_period=subscribtion_period
        )
        await message.answer(
            SUBSCRIBTION_CREATE.format(
                end_date=subscribtion.end_date.strftime(FORMAT)
            )
        )
        link = await bot.create_chat_invite_link(
            chat_id=int(settings.group_id),
            creates_join_request=True,
            expire_date=LINK_EXPIRE_TIME
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text=INVITE.format(link=link.invite_link)
        )


@router.message(CommandStart(), IsPrivate())
async def send_instructions(message: Message):
    await message.answer(
        text=START_MESSAGE,
        reply_markup=choose_action_keyboard
    )
